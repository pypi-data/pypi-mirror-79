import os
import time

from libpipe import futils

from . import skymodel, cal
from .settings import Settings


default_calpipe_filename = 'calpipe.toml'


def get_all_tasks():
    d = {}
    for klass in AbstractTask.__subclasses__():
        if hasattr(klass, 'name'):
            d[klass.name] = klass
    return d


def get_all_tasks_descriptions():
    d = {}
    for klass in AbstractTask.__subclasses__():
        if hasattr(klass, 'name') and hasattr(klass, 'desc'):
            d[klass.name] = klass.desc
    return d


class AbstractTask(object):

    def __init__(self, settings_obj):
        self.settings = settings_obj

    def run(self, msins):
        pass


class Init(AbstractTask):

    name = 'init'
    desc = 'Create new configuration'

    def __init__(self, settings_obj):
        AbstractTask.__init__(self, settings_obj)

    def run(self, msins):
        if os.path.exists(default_calpipe_filename):
            print(f'Error: configuration file {default_calpipe_filename} alread exist.')
            return msins
        print(f'Default configuration created in {default_calpipe_filename} ...')
        Settings.get_defaults().save(default_calpipe_filename)
        return msins


class BuildSkyModel(AbstractTask):

    name = 'build_sky_model'
    desc = 'Build sky model'

    def __init__(self, settings_obj):
        AbstractTask.__init__(self, settings_obj)

    def run(self, msins):
        s_bsm = self.settings.build_sky_model
        s_worker = self.settings.worker

        if s_bsm.int_sky_model in skymodel.sky_model_catalogs:
            int_sky_model = f'catalog_intrinsic_{s_bsm.int_sky_model}.skymodel'
            skymodel.build_sky_model_ms(msins[0], s_bsm.min_flux, s_bsm.catalog_radius, int_sky_model,
                                        catalog=s_bsm.int_sky_model)
        elif os.path.exists(s_bsm.int_sky_model):
            int_sky_model = s_bsm.int_sky_model
        else:
            print('Intrinsic sky model not found')
            return []

        cal.MakeAppSkyModel(s_worker, int_sky_model, s_bsm).run(msins)
        cal.MakeSourceDB(s_worker, s_bsm).run(msins)

        return msins


class InitialCal(AbstractTask):

    name = 'init_cal'
    desc = 'Initial direction dependent calibration'

    def __init__(self, settings_obj):
        AbstractTask.__init__(self, settings_obj)

    def run(self, msins):
        s_worker = self.settings.worker
        max_time = self.settings.init_cal.max_sub_time
        cal_settings = cal.CalSettings(**self.settings.init_cal)
        sky_model = cal.SkyModel(self.settings.build_sky_model.app_sky_model_name)

        cal.RestoreOrBackupFlag(s_worker).run(msins)
        cal.DDEcal(s_worker, cal_settings, sky_model).run(msins)
        cal.SubtractAteam(s_worker, cal_settings, sky_model, 'DATA', 'CORRECTED_DATA', max_time=max_time).run(msins)
        cal.ApplyCal(s_worker, cal_settings, 'CORRECTED_DATA', 'CORRECTED_DATA').run(msins)

        cal.PlotSolutions(s_worker, cal_settings.parmdb).run(msins)

        return msins


class PostCalFlag(AbstractTask):

    name = 'post_cal_flag'
    desc = 'Post calibration flagging'

    def __init__(self, settings_obj):
        AbstractTask.__init__(self, settings_obj)

    def run(self, msins):
        s_worker = self.settings.worker
        s_flag = self.settings.post_cal_flag

        cal.RestoreOrBackupFlag(s_worker, flag_name='post_cal_flag.h5').run(msins)

        if s_flag.do_aoflagger:
            cal.FlagPostCal(s_worker, s_flag.aoflagger_strategy).run(msins)

        if s_flag.do_badbaselines:
            cal.AoQuality(s_worker).run(msins)
            cal.FlagBadBaselines(s_worker, nsigma_stations=s_flag.nsigma_stations,
                                 nsigma_baselines=s_flag.nsigma_baselines).run(msins)

        if s_flag.do_ssins:
            cal.SSINSFlagger(s_worker, config=s_flag.ssins_seetings, plot_dir='flag_plot').run(msins)

        if s_flag.do_scans_flagging:
            print('Start scans flagging ...')
            flagutils.flag_badscans(msins, data_col='CORRECTED_DATA', nsigma=s_flag.nsigma_scans)

        cal.AoQuality(s_worker).run(msins)

        return msins


class SmoothSolutions(AbstractTask):

    name = 'smooth_sol'
    desc = 'Smooth Solutions'

    def __init__(self, settings_obj):
        AbstractTask.__init__(self, settings_obj)

    def run(self, msins):
        from .smoothsol import smooth_solutions

        s_smooth = self.settings.smooth_sol
        smooth_solutions(msins, s_smooth.parmdb_in, s_smooth.parmdb_out, plot_dir=s_smooth.plot_dir)

        return msins


class ApplySolutin(AbstractTask):

    name = 'apply_sol'
    desc = 'Apply Solutions'

    def __init__(self, settings_obj):
        AbstractTask.__init__(self, settings_obj)

    def run(self, msins):
        s_apply = self.settings.apply_sol
        s_worker = self.settings.worker
        cal_settings = cal.CalSettings(parmdb=s_apply.parmdb, cal_mode=s_apply.cal_mode)

        cal.ApplyCal(s_worker, cal_settings, 'DATA', 'CORRECTED_DATA').run(msins)

        return msins


class PeelCal(AbstractTask):

    name = 'peel'
    desc = 'Peel calibration'

    def __init__(self, settings_obj):
        AbstractTask.__init__(self, settings_obj)

    def run(self, msins):
        s_worker = self.settings.worker
        s_peel = self.settings.peel
        cal_settings_init = cal.CalSettings(parmdb=s_peel.init_parmdb, cal_mode=s_peel.init_cal_mode)
        sky_model = cal.SkyModel(self.settings.build_sky_model.app_sky_model_name)

        # Start with a new MS
        msouts = cal.CopyMS(s_worker, 'DATA', s_peel.ms_postfix).run(msins)

        # Copy initial calibration table from .MS to _PEEL.MS
        futils.zip_copy(msins, msouts, cal_settings_init.parmdb)
        sky_model.copy(msins, msouts)

        for i, mspeel in cal.Peel(sky_model).iterations(msouts):
            cal_settings_iter = cal.CalSettings(**s_peel)
            cal_settings_iter.parmdb = f'instrument_peel_iter{i}.h5'

            if s_peel.phase_shift:
                mstemps = cal.PeelPreSubtractPhaseShifted(i, s_worker, cal_settings_init, sky_model,
                                                          time_avg=s_peel.phase_shift_time_avg,
                                                          freq_avg=s_peel.phase_shift_freq_avg,
                                                          max_time=s_peel.max_sub_time).run(mspeel)

                sky_model.copy(mspeel, mstemps)
                cal.PeelCal(i, s_worker, cal_settings_iter, sky_model, data_col='DATA').run(mstemps)

                while 1:
                    try:
                        futils.zip_copy(mstemps, mspeel, cal_settings_iter.parmdb)
                        break
                    except FileNotFoundError:
                        print('Error copying file, while try in a second ...')
                        time.sleep(1)
                futils.zip_rm(mstemps)

                mstemps = cal.PeelPostSubtractPhaseShift(i, s_worker, cal_settings_iter, sky_model).run(mspeel)

                os.sync()
                time.sleep(1)
                futils.zip_rename_reg(mspeel, mstemps, 'table|^[A-Z]', invert=True)
                futils.zip_rm(mspeel)
                futils.zip_rename(mstemps, mspeel)
            else:
                cal.PeelPreSubtract(i, s_worker, cal_settings_init, sky_model, max_time=s_peel.max_sub_time).run(mspeel)
                cal.PeelCal(i, s_worker, cal_settings_iter, sky_model).run(mspeel)
                cal.PeelPostSubtract(i, s_worker, cal_settings_iter, sky_model).run(mspeel)

            # cal.PlotSolutions(s_worker, cal_settings_iter.parmdb).run(mspeel)

        return msouts


class DICal(AbstractTask):

    name = 'dical'
    desc = 'Direction independent calibration'

    def __init__(self, settings_obj):
        AbstractTask.__init__(self, settings_obj)

    def run(self, msins):
        s_worker = self.settings.worker
        cal_settings = cal.CalSettings(**self.settings.dical)
        sky_model = cal.SkyModel(self.settings.build_sky_model.app_sky_model_name)

        mstemps = cal.DDEcalAvg(s_worker, cal_settings, sky_model,
                                time_avg=self.settings.dical.time_avg,
                                freq_avg=self.settings.dical.freq_avg).run(msins)
        futils.zip_rm(mstemps)
        cal.ApplyCal(s_worker, cal_settings, 'DATA', 'CORRECTED_DATA').run(msins)

        return msins
