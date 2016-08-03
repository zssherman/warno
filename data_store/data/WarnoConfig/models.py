from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from flask_user.forms import RegisterForm
from flask_wtf import Form
from wtforms import StringField, SubmitField, validators
from flask_user import UserMixin

db = SQLAlchemy()


# Non-Database Models
class MyRegisterForm(RegisterForm):
    name = StringField('Name', validators=[validators.DataRequired('Name is required.')])


# Define the User profile form
class UserProfileForm(Form):
    name = StringField('Name', validators=[
        validators.DataRequired('Name is required')])
    submit = SubmitField('Save')


# Database Models
class Site(db.Model):
    __tablename__ = 'sites'

    id = db.Column("site_id", db.Integer, primary_key=True)
    name_short = db.Column(db.String(8), nullable=False)
    name_long = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    facility = db.Column(db.String(32))
    mobile = db.Column(db.Boolean)
    location_name = db.Column(db.String)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column("user_id", db.Integer, primary_key=True)

    # Authentication
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    # Email info
    email = db.Column("email", db.String)
    confirmed_at = db.Column(db.DateTime())

    # User Information
    is_active = db.Column('is_active', db.Boolean(), nullable=False, server_default="0")
    name = db.Column(db.String, nullable=False, server_default='')
    location = db.Column(db.String)
    position = db.Column(db.String)
    authorizations = db.Column(db.String)

    def get_id(self):
        return unicode(self.id)

    def has_confirmed_email(self):
        return True

    def is_authenticated(self):
        return True


class EventCode(db.Model):
    __tablename__ = "event_codes"

    event_code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)


class Instrument(db.Model):
    __tablename__ = "instruments"

    id = db.Column("instrument_id", db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.site_id'))
    name_short = db.Column(db.String(32))
    name_long = db.Column(db.String)
    type = db.Column(db.String)
    vendor = db.Column(db.String)
    description = db.Column(db.String)
    frequency_band = db.Column(db.String(2))
    site = db.relationship(Site)


class InstrumentLog(db.Model):
    __tablename__ = "instrument_logs"

    id = db.Column("log_number", db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instrument_id'))
    contents = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    status = db.Column(db.Integer)
    supporting_images = db.Column(db.String)
    instrument = db.relationship(Instrument)
    author = db.relationship(User)


class TableReference(db.Model):
    __tablename__ = "table_references"

    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instrument_id'), primary_key=True)
    referenced_tables = db.Column(postgresql.ARRAY(db.String))
    instrument = db.relationship(Instrument)


class InstrumentDataReference(db.Model):
    __tablename__ = "instrument_data_references"

    id = db.Column(db.Integer, primary_key=True)
    instrument_id = db.Column(db.ForeignKey('instruments.instrument_id'), nullable=False)
    special = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String)
    instrument = db.relationship(Instrument)


class PulseCapture(db.Model):
    __tablename__ = "pulse_captures"

    id = db.Column(db.Integer, primary_key=True)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instrument_id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    data = db.Column(postgresql.ARRAY(db.Float))
    instrument = db.relationship(Instrument)


class ValidColumn(db.Model):
    __tablename__ = "valid_columns"

    id = db.Column(db.Integer, primary_key=True)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instrument_id'), nullable=False)
    table_name = db.Column(db.String, nullable=False)
    column_name = db.Column(db.String, nullable=False)


class Alias(db.Model):
    __tablename__ = "aliases"

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String, nullable=False)
    column_name = db.Column(db.String, nullable=False)
    name_short = db.Column(db.String, nullable=False)
    name_long = db.Column(db.String)
    unit = db.Column(db.String)
    role = db.Column(db.String)


class EventWithText(db.Model):
    __tablename__ = "events_with_text"

    id = db.Column(db.Integer, primary_key=True)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instrument_id'), nullable=False)
    event_code_id = db.Column("event_code", db.Integer, db.ForeignKey('event_codes.event_code'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.String)
    instrument = db.relationship(Instrument)
    event_code = db.relationship(EventCode)


class EventWithValue(db.Model):
    __tablename__ = "events_with_value"

    id = db.Column(db.Integer, primary_key=True)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instrument_id'), nullable=False)
    event_code_id = db.Column("event_code", db.Integer, db.ForeignKey('event_codes.event_code'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float)
    instrument = db.relationship(Instrument)
    event_code = db.relationship(EventCode)


class ProsensingPAF(db.Model):
    __tablename__ = "prosensing_paf"
    id = db.Column("packet_id", db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.site_id'), nullable=False)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.instrument_id'), nullable=False)

    site = db.relationship(Site)
    instrument = db.relationship(Instrument)

    ad_skip_count = db.Column(db.Integer)
    ad_skip_count_override = db.Column(db.Integer)
    ad_skip_count_use_override = db.Column(db.Integer)
    amplifier_drive_power_burst_a_dbm = db.Column(db.Float)
    amplifier_drive_power_burst_b_dbm = db.Column(db.Float)
    amplifier_drive_power_chirp_a_dbm = db.Column(db.Float)
    amplifier_drive_power_chirp_b_dbm = db.Column(db.Float)
    amplifier_output_power_burst_a_dbm = db.Column(db.Float)
    amplifier_output_power_burst_b_dbm = db.Column(db.Float)
    amplifier_output_power_chirp_a_dbm = db.Column(db.Float)
    amplifier_output_power_chirp_b_dbm = db.Column(db.Float)
    amplitude_scaling_burst_a = db.Column(db.Float)
    amplitude_scaling_burst_b = db.Column(db.Float)
    amplitude_scaling_chirp_a = db.Column(db.Float)
    amplitude_scaling_chirp_b = db.Column(db.Float)
    antenna_humidity = db.Column(db.Float)
    antenna_temp = db.Column(db.Float)
    asp_communication_error = db.Column(db.String)
    asp_connection = db.Column(db.String)
    asp_connection_error = db.Column(db.String)
    asp_custom_waveform_file_path_burst_a = db.Column(db.String)
    asp_custom_waveform_file_path_burst_b = db.Column(db.String)
    asp_custom_waveform_file_path_chirp_a = db.Column(db.String)
    asp_custom_waveform_file_path_chirp_b = db.Column(db.String)
    asp_status_summary = db.Column(db.String)
    asp_trig_delay_burst_a = db.Column(db.Float)
    asp_trig_delay_burst_a_override = db.Column(db.Integer)
    asp_trig_delay_burst_a_use_override = db.Column(db.Integer)
    asp_trig_delay_burst_b = db.Column(db.Float)
    asp_trig_delay_burst_b_override = db.Column(db.Integer)
    asp_trig_delay_burst_b_use_override = db.Column(db.Integer)
    asp_trig_delay_chirp_a = db.Column(db.Float)
    asp_trig_delay_chirp_a_override = db.Column(db.Integer)
    asp_trig_delay_chirp_a_use_override = db.Column(db.Integer)
    asp_trig_delay_chirp_b = db.Column(db.Float)
    asp_trig_delay_chirp_b_override = db.Column(db.Integer)
    asp_trig_delay_chirp_b_use_override = db.Column(db.Integer)
    asp_unrecognized_firmware = db.Column(db.String)
    asp_waveform_burst_a = db.Column(db.String)
    asp_waveform_burst_b = db.Column(db.String)
    asp_waveform_chirp_a = db.Column(db.String)
    asp_waveform_chirp_b = db.Column(db.String)
    attenuation_db_burst_a = db.Column(db.Integer)
    attenuation_db_burst_b = db.Column(db.Integer)
    attenuation_db_chirp_a = db.Column(db.Integer)
    attenuation_db_chirp_b = db.Column(db.Integer)
    auto_calculate_noise_regions = db.Column(db.Integer)
    auto_calculate_signal_regions = db.Column(db.Integer)
    bandwidth_burst_a = db.Column(db.Float)
    bandwidth_burst_b = db.Column(db.Float)
    bandwidth_chirp_a = db.Column(db.Float)
    bandwidth_chirp_b = db.Column(db.Float)
    cal_constant_burst_a_copol = db.Column(db.Float)
    cal_constant_burst_a_crosspol = db.Column(db.Float)
    cal_constant_burst_b_copol = db.Column(db.Float)
    cal_constant_burst_b_crosspol = db.Column(db.Float)
    cal_constant_chirp_a_copol = db.Column(db.Float)
    cal_constant_chirp_a_crosspol = db.Column(db.Float)
    cal_constant_chirp_b_copol = db.Column(db.Float)
    cal_constant_chirp_b_crosspol = db.Column(db.Float)
    cal_switch_enabled = db.Column(db.Integer)
    cal_switch_enabled_effective = db.Column(db.Integer)
    center_main_bang_burst_a = db.Column(db.Float)
    center_main_bang_burst_b = db.Column(db.Float)
    center_main_bang_chirp_a = db.Column(db.Float)
    center_main_bang_chirp_b = db.Column(db.Float)
    clutter_avg_len_a = db.Column(db.Integer)
    clutter_avg_len_b = db.Column(db.Integer)
    clutter_filter_enabled = db.Column(db.Integer)
    coherent_on_recv_enabled = db.Column(db.Integer)
    coherent_on_recv_gate_burst_a = db.Column(db.Integer)
    coherent_on_recv_gate_burst_b = db.Column(db.Integer)
    coherent_on_recv_gate_chirp_a = db.Column(db.Integer)
    coherent_on_recv_gate_chirp_b = db.Column(db.Integer)
    cold_noise_mw_burst_a_copol = db.Column(db.Float)
    cold_noise_mw_burst_a_crosspol = db.Column(db.Float)
    cold_noise_mw_burst_b_copol = db.Column(db.Float)
    cold_noise_mw_burst_b_crosspol = db.Column(db.Float)
    cold_noise_mw_chirp_a_copol = db.Column(db.Float)
    cold_noise_mw_chirp_a_crosspol = db.Column(db.Float)
    cold_noise_mw_chirp_b_copol = db.Column(db.Float)
    cold_noise_mw_chirp_b_crosspol = db.Column(db.Float)
    cold_noise_region_n_gates = db.Column(db.Integer)
    cold_noise_region_n_gates_override = db.Column(db.Integer)
    cold_noise_region_start_gate = db.Column(db.Integer)
    cold_noise_region_start_gate_override = db.Column(db.Integer)
    coolant_return_temp = db.Column(db.Float)
    coolant_supply_temp = db.Column(db.Float)
    data_trimming_enabled = db.Column(db.Integer)
    digrcv_filter_bandwidth_ch1 = db.Column(db.Float)
    digrcv_filter_bandwidth_ch2 = db.Column(db.Float)
    digrcv_filter_bandwidth_ch3 = db.Column(db.Float)
    digrcv_filter_bandwidth_ch4 = db.Column(db.Float)
    digrcv_filter_bandwidth_effective_ch1 = db.Column(db.Float)
    digrcv_filter_bandwidth_effective_ch2 = db.Column(db.Float)
    digrcv_filter_bandwidth_effective_ch3 = db.Column(db.Float)
    digrcv_filter_bandwidth_effective_ch4 = db.Column(db.Float)
    digrcv_fir_dec = db.Column(db.Integer)
    digrcv_fir_dec_effective = db.Column(db.Integer)
    digrcv_fir_filter_delay = db.Column(db.Float)
    eight_vdc = db.Column(db.Float)
    eika_temp = db.Column(db.Float)
    ems_1_override = db.Column(db.Integer)
    ems_1_override_effective = db.Column(db.Integer)
    ems_2_override = db.Column(db.Integer)
    ems_2_override_effective = db.Column(db.Integer)
    ems_delay = db.Column(db.Float)
    ems_delay_override = db.Column(db.Float)
    ems_delay_use_override = db.Column(db.Integer)
    ems_use_override = db.Column(db.Integer)
    ems_use_override_effective = db.Column(db.Integer)
    fft_len_a = db.Column(db.Integer)
    fft_len_b = db.Column(db.Integer)
    fft_taper = db.Column(db.Integer)
    fifteen_vdc = db.Column(db.Float)
    five_point_two_vdc = db.Column(db.Float)
    five_vdc = db.Column(db.Float)
    group_b_enabled = db.Column(db.Integer)
    group_b_enabled_effective = db.Column(db.Integer)
    hot_noise_mw_burst_a_copol = db.Column(db.Float)
    hot_noise_mw_burst_a_crosspol = db.Column(db.Float)
    hot_noise_mw_burst_b_copol = db.Column(db.Float)
    hot_noise_mw_burst_b_crosspol = db.Column(db.Float)
    hot_noise_mw_chirp_a_copol = db.Column(db.Float)
    hot_noise_mw_chirp_a_crosspol = db.Column(db.Float)
    hot_noise_mw_chirp_b_copol = db.Column(db.Float)
    hot_noise_mw_chirp_b_crosspol = db.Column(db.Float)
    hot_noise_region_n_gates = db.Column(db.Integer)
    hot_noise_region_n_gates_override = db.Column(db.Integer)
    hot_noise_region_start_gate = db.Column(db.Integer)
    hot_noise_region_start_gate_override = db.Column(db.Integer)
    incl_pitch = db.Column(db.Float)
    incl_roll = db.Column(db.Float)
    lna_copol_temp = db.Column(db.Float)
    lna_xpol_temp = db.Column(db.Float)
    max_sampled_range_burst_a = db.Column(db.Float)
    max_sampled_range_burst_b = db.Column(db.Float)
    max_sampled_range_chirp_a = db.Column(db.Float)
    max_sampled_range_chirp_b = db.Column(db.Float)
    max_velocity_m_sec_burst_a = db.Column(db.Float)
    max_velocity_m_sec_burst_b = db.Column(db.Float)
    max_velocity_m_sec_chirp_a = db.Column(db.Float)
    max_velocity_m_sec_chirp_b = db.Column(db.Float)
    minus_five_vdc = db.Column(db.Float)
    mod_blanked = db.Column(db.Integer)
    mod_fault_time = db.Column(db.Float)
    mod_has_fault = db.Column(db.Integer)
    mod_high_voltage_on = db.Column(db.Integer)
    mod_power_on = db.Column(db.Integer)
    mod_transmitting = db.Column(db.Integer)
    mod_warming_up = db.Column(db.Integer)
    modulator_external_temp = db.Column(db.Float)
    modulator_fault_interlock = db.Column(db.Integer)
    modulator_fault_mod = db.Column(db.Integer)
    modulator_fault_sum = db.Column(db.Integer)
    modulator_fault_sync = db.Column(db.Integer)
    modulator_fault_time_interlock = db.Column(db.Integer)
    modulator_fault_time_mod = db.Column(db.Integer)
    modulator_fault_time_sum = db.Column(db.Integer)
    modulator_fault_time_sync = db.Column(db.Integer)
    modulator_fault_time_transmitter_temp = db.Column(db.Integer)
    modulator_fault_transmitter_temp = db.Column(db.Integer)
    modulator_filament_delay = db.Column(db.Integer)
    modulator_hv_on_command = db.Column(db.Integer)
    modulator_power_on_command = db.Column(db.Integer)
    modulator_power_valid = db.Column(db.Integer)
    modulator_sync_divider = db.Column(db.Integer)
    modulator_sync_enabled = db.Column(db.Integer)
    modulator_sync_frequency = db.Column(db.Integer)
    modulator_temp = db.Column(db.Float)
    moments_fixed_roi_width_m_sec = db.Column(db.Integer)
    moments_power_threshold_db = db.Column(db.Float)
    moments_roi_mode = db.Column(db.Integer)
    n_gates = db.Column(db.Integer)
    n_gates_proc_burst_a = db.Column(db.Integer)
    n_gates_proc_burst_b = db.Column(db.Integer)
    n_gates_proc_chirp_a = db.Column(db.Integer)
    n_gates_proc_chirp_b = db.Column(db.Integer)
    n_group_pulses_a = db.Column(db.Integer)
    n_group_pulses_b = db.Column(db.Integer)
    noise_delay = db.Column(db.Float)
    noise_delay_override = db.Column(db.Float)
    noise_delay_use_override = db.Column(db.Integer)
    noise_figure_db_burst_a_copol = db.Column(db.Float)
    noise_figure_db_burst_a_crosspol = db.Column(db.Float)
    noise_figure_db_burst_b_copol = db.Column(db.Float)
    noise_figure_db_burst_b_crosspol = db.Column(db.Float)
    noise_figure_db_chirp_a_copol = db.Column(db.Float)
    noise_figure_db_chirp_a_crosspol = db.Column(db.Float)
    noise_figure_db_chirp_b_copol = db.Column(db.Float)
    noise_figure_db_chirp_b_crosspol = db.Column(db.Float)
    noise_region_n_gates_nominal = db.Column(db.Integer)
    noise_scale_factor_burst_a = db.Column(db.Float)
    noise_scale_factor_burst_b = db.Column(db.Float)
    noise_scale_factor_chirp_a = db.Column(db.Float)
    noise_scale_factor_chirp_b = db.Column(db.Float)
    noise_scale_factor_effective_burst_a = db.Column(db.Float)
    noise_scale_factor_effective_burst_b = db.Column(db.Float)
    noise_scale_factor_effective_chirp_a = db.Column(db.Float)
    noise_scale_factor_effective_chirp_b = db.Column(db.Float)
    noise_width = db.Column(db.Float)
    noise_width_override = db.Column(db.Integer)
    noise_width_use_override = db.Column(db.Integer)
    outside_air_temp = db.Column(db.Float)
    pentek_open = db.Column(db.String)
    pentek_open_failed = db.Column(db.String)
    pentek_receiving_data = db.Column(db.String)
    pentek_run_failed = db.Column(db.String)
    pentek_running = db.Column(db.String)
    pentek_status_summary = db.Column(db.String)
    plo1_lock_status = db.Column(db.Integer)
    plo2_lock_status = db.Column(db.Integer)
    plo3_lock_status = db.Column(db.Integer)
    plo4_lock_status = db.Column(db.Integer)
    post_avg_len = db.Column(db.Integer)
    power_supply_temp = db.Column(db.Float)
    pri_a = db.Column(db.Float)
    pri_b = db.Column(db.Float)
    pulse_compression_ratio_burst_a = db.Column(db.Float)
    pulse_compression_ratio_burst_b = db.Column(db.Float)
    pulse_compression_ratio_chirp_a = db.Column(db.Float)
    pulse_compression_ratio_chirp_b = db.Column(db.Float)
    pulse_compression_ratio_effective_burst_a = db.Column(db.Float)
    pulse_compression_ratio_effective_burst_b = db.Column(db.Float)
    pulse_compression_ratio_effective_chirp_a = db.Column(db.Float)
    pulse_compression_ratio_effective_chirp_b = db.Column(db.Float)
    range_gate_spacing = db.Column(db.Float)
    range_gate_spacing_proc = db.Column(db.Float)
    range_resolution_burst_a = db.Column(db.Float)
    range_resolution_burst_b = db.Column(db.Float)
    range_resolution_chirp_a = db.Column(db.Float)
    range_resolution_chirp_b = db.Column(db.Float)
    range_resolution_effective_burst_a = db.Column(db.Float)
    range_resolution_effective_burst_b = db.Column(db.Float)
    range_resolution_effective_chirp_a = db.Column(db.Float)
    range_resolution_effective_chirp_b = db.Column(db.Float)
    rcb_communication_error = db.Column(db.String)
    rcb_connection = db.Column(db.String)
    rcb_connection_error = db.Column(db.String)
    rcb_humidity = db.Column(db.Float)
    rcb_status_summary = db.Column(db.String)
    rcb_status_valid = db.Column(db.Integer)
    rcb_temp = db.Column(db.Float)
    rcb_unrecognized_firmware = db.Column(db.String)
    reverse_pwr_load_temp = db.Column(db.Float)
    rf_unit_output_power_burst_a_dbm = db.Column(db.Float)
    rf_unit_output_power_burst_b_dbm = db.Column(db.Float)
    rf_unit_output_power_chirp_a_dbm = db.Column(db.Float)
    rf_unit_output_power_chirp_b_dbm = db.Column(db.Float)
    rf_unit_temp = db.Column(db.Float)
    rtd14 = db.Column(db.Float)
    rtd15 = db.Column(db.Float)
    rtd16 = db.Column(db.Float)
    rtd6 = db.Column(db.Float)
    rtd7 = db.Column(db.Float)
    rtd8 = db.Column(db.Float)
    rx_gain_db_burst_a_copol = db.Column(db.Float)
    rx_gain_db_burst_a_crosspol = db.Column(db.Float)
    rx_gain_db_burst_b_copol = db.Column(db.Float)
    rx_gain_db_burst_b_crosspol = db.Column(db.Float)
    rx_gain_db_chirp_a_copol = db.Column(db.Float)
    rx_gain_db_chirp_a_crosspol = db.Column(db.Float)
    rx_gain_db_chirp_b_copol = db.Column(db.Float)
    rx_gain_db_chirp_b_crosspol = db.Column(db.Float)
    scope_communication_error = db.Column(db.String)
    scope_connection = db.Column(db.String)
    scope_connection_error = db.Column(db.String)
    scope_lookup_table_missing = db.Column(db.String)
    scope_status_summary = db.Column(db.String)
    server_mode = db.Column(db.Integer)
    server_state = db.Column(db.Integer)
    signal_region_n_gates_a = db.Column(db.Integer)
    signal_region_n_gates_a_override = db.Column(db.Integer)
    signal_region_n_gates_b = db.Column(db.Integer)
    signal_region_n_gates_b_override = db.Column(db.Integer)
    signal_region_start_gate_a = db.Column(db.Integer)
    signal_region_start_gate_a_override = db.Column(db.Integer)
    signal_region_start_gate_b = db.Column(db.Integer)
    signal_region_start_gate_b_override = db.Column(db.Integer)
    sky_noise_mw_burst_a_copol = db.Column(db.Float)
    sky_noise_mw_burst_a_crosspol = db.Column(db.Float)
    sky_noise_mw_burst_b_copol = db.Column(db.Float)
    sky_noise_mw_burst_b_crosspol = db.Column(db.Float)
    sky_noise_mw_chirp_a_copol = db.Column(db.Float)
    sky_noise_mw_chirp_a_crosspol = db.Column(db.Float)
    sky_noise_mw_chirp_b_copol = db.Column(db.Float)
    sky_noise_mw_chirp_b_crosspol = db.Column(db.Float)
    sky_noise_region_n_gates = db.Column(db.Integer)
    sky_noise_region_n_gates_override = db.Column(db.Integer)
    sky_noise_region_start_gate = db.Column(db.Integer)
    sky_noise_region_start_gate_override = db.Column(db.Integer)
    software_dec = db.Column(db.Integer)
    software_filter_burst_a = db.Column(db.String)
    software_filter_burst_b = db.Column(db.String)
    software_filter_chirp_a = db.Column(db.String)
    software_filter_chirp_b = db.Column(db.String)
    software_filter_file_path_burst_a = db.Column(db.String)
    software_filter_file_path_burst_b = db.Column(db.String)
    software_filter_file_path_chirp_a = db.Column(db.String)
    software_filter_file_path_chirp_b = db.Column(db.String)
    software_filter_output_trimming_power_threshold = db.Column(db.Float)
    tukey_coef_burst_a = db.Column(db.Float)
    tukey_coef_burst_b = db.Column(db.Float)
    tukey_coef_chirp_a = db.Column(db.Float)
    tukey_coef_chirp_b = db.Column(db.Float)
    tukey_coef_effective_burst_a = db.Column(db.Float)
    tukey_coef_effective_burst_b = db.Column(db.Float)
    tukey_coef_effective_chirp_a = db.Column(db.Float)
    tukey_coef_effective_chirp_b = db.Column(db.Float)
    tukey_correction_burst_a = db.Column(db.Float)
    tukey_correction_burst_b = db.Column(db.Float)
    tukey_correction_chirp_a = db.Column(db.Float)
    tukey_correction_chirp_b = db.Column(db.Float)
    twelve_vdc = db.Column(db.Float)
    twenty_eight_vdc = db.Column(db.Float)
    tx_freq_burst = db.Column(db.Float)
    tx_freq_chirp = db.Column(db.Float)
    tx_pulse_bracketing = db.Column(db.Float)
    tx_pulse_n_gates_burst_a = db.Column(db.Integer)
    tx_pulse_n_gates_burst_b = db.Column(db.Integer)
    tx_pulse_n_gates_chirp_a = db.Column(db.Integer)
    tx_pulse_n_gates_chirp_b = db.Column(db.Integer)
    tx_pulse_start_gate_burst_a = db.Column(db.Integer)
    tx_pulse_start_gate_burst_b = db.Column(db.Integer)
    tx_pulse_start_gate_chirp_a = db.Column(db.Integer)
    tx_pulse_start_gate_chirp_b = db.Column(db.Integer)
    tx_pulse_width_a = db.Column(db.Float)
    tx_pulse_width_b = db.Column(db.Float)
    tx_trigger_delay = db.Column(db.Float)
    tx_trigger_enabled = db.Column(db.Integer)
    tx_trigger_enabled_effective = db.Column(db.Integer)
    use_digrcv_default_filter_ch1 = db.Column(db.Integer)
    use_digrcv_default_filter_ch2 = db.Column(db.Integer)
    use_digrcv_default_filter_ch3 = db.Column(db.Integer)
    use_digrcv_default_filter_ch4 = db.Column(db.Integer)
    use_digrcv_default_filter_effective_ch1 = db.Column(db.Integer)
    use_digrcv_default_filter_effective_ch2 = db.Column(db.Integer)
    use_digrcv_default_filter_effective_ch3 = db.Column(db.Integer)
    use_digrcv_default_filter_effective_ch4 = db.Column(db.Integer)
    use_software_filter_parameters = db.Column(db.Integer)
    velocity_spacing_m_sec_burst_a = db.Column(db.Float)
    velocity_spacing_m_sec_burst_b = db.Column(db.Float)
    velocity_spacing_m_sec_chirp_a = db.Column(db.Float)
    velocity_spacing_m_sec_chirp_b = db.Column(db.Float)
    width_burst_a = db.Column(db.Float)
    width_burst_b = db.Column(db.Float)
    width_chirp_a = db.Column(db.Float)
    width_chirp_b = db.Column(db.Float)
    zero_gate_range_proc_burst_a = db.Column(db.Float)
    zero_gate_range_proc_burst_b = db.Column(db.Float)
    zero_gate_range_proc_chirp_a = db.Column(db.Float)
    zero_gate_range_proc_chirp_b = db.Column(db.Float)
    zero_gate_time = db.Column(db.Float)
    zero_raw_gate_range_burst_a = db.Column(db.Float)
    zero_raw_gate_range_burst_b = db.Column(db.Float)
    zero_raw_gate_range_chirp_a = db.Column(db.Float)
    zero_raw_gate_range_chirp_b = db.Column(db.Float)
    zero_raw_gate_range_offset_burst_a = db.Column(db.Integer)
    zero_raw_gate_range_offset_burst_b = db.Column(db.Integer)
    zero_raw_gate_range_offset_chirp_a = db.Column(db.Integer)
    zero_raw_gate_range_offset_chirp_b = db.Column(db.Integer)
