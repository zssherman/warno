"""Base

Revision ID: ac055fa10741
Revises: 
Create Date: 2016-03-14 15:39:57.319860

"""

# revision identifiers, used by Alembic.
revision = 'ac055fa10741'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_codes',
    sa.Column('event_code', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('event_code')
    )
    op.create_table('sites',
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('name_short', sa.String(length=8), nullable=False),
    sa.Column('name_long', sa.String(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('facility', sa.String(length=8), nullable=True),
    sa.Column('mobile', sa.Boolean(), nullable=True),
    sa.Column('location_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('site_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('e-mail', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('authorizations', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('instruments',
    sa.Column('instrument_id', sa.Integer(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=True),
    sa.Column('name_short', sa.String(length=8), nullable=True),
    sa.Column('name_long', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('vendor', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('frequency_band', sa.String(length=2), nullable=True),
    sa.ForeignKeyConstraint(['site_id'], ['sites.site_id'], ),
    sa.PrimaryKeyConstraint('instrument_id')
    )
    op.create_table('events_with_text',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instrument_id', sa.Integer(), nullable=False),
    sa.Column('event_code', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['event_code'], ['event_codes.event_code'], ),
    sa.ForeignKeyConstraint(['instrument_id'], ['instruments.instrument_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('events_with_value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instrument_id', sa.Integer(), nullable=False),
    sa.Column('event_code', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('value', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['event_code'], ['event_codes.event_code'], ),
    sa.ForeignKeyConstraint(['instrument_id'], ['instruments.instrument_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('instrument_data_references',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instrument_id', sa.Integer(), nullable=False),
    sa.Column('special', sa.Boolean(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['instrument_id'], ['instruments.instrument_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('instrument_logs',
    sa.Column('log_number', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('instrument_id', sa.Integer(), nullable=True),
    sa.Column('contents', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('supporting_images', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.user_id'], ),
    sa.ForeignKeyConstraint(['instrument_id'], ['instruments.instrument_id'], ),
    sa.PrimaryKeyConstraint('log_number')
    )
    op.create_table('prosensing_paf',
    *[sa.Column('packet_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('instrument_id', sa.Integer(), nullable=False),
    sa.Column('ad_skip_count', sa.Integer(), nullable=True),
    sa.Column('ad_skip_count_override', sa.Integer(), nullable=True),
    sa.Column('ad_skip_count_use_override', sa.Integer(), nullable=True),
    sa.Column('amplifier_drive_power_burst_a_dbm', sa.Float(), nullable=True),
    sa.Column('amplifier_drive_power_burst_b_dbm', sa.Float(), nullable=True),
    sa.Column('amplifier_drive_power_chirp_a_dbm', sa.Float(), nullable=True),
    sa.Column('amplifier_drive_power_chirp_b_dbm', sa.Float(), nullable=True),
    sa.Column('amplifier_output_power_burst_a_dbm', sa.Float(), nullable=True),
    sa.Column('amplifier_output_power_burst_b_dbm', sa.Float(), nullable=True),
    sa.Column('amplifier_output_power_chirp_a_dbm', sa.Float(), nullable=True),
    sa.Column('amplifier_output_power_chirp_b_dbm', sa.Float(), nullable=True),
    sa.Column('amplitude_scaling_burst_a', sa.Float(), nullable=True),
    sa.Column('amplitude_scaling_burst_b', sa.Float(), nullable=True),
    sa.Column('amplitude_scaling_chirp_a', sa.Float(), nullable=True),
    sa.Column('amplitude_scaling_chirp_b', sa.Float(), nullable=True),
    sa.Column('antenna_humidity', sa.Float(), nullable=True),
    sa.Column('antenna_temp', sa.Float(), nullable=True),
    sa.Column('asp_communication_error', sa.String(), nullable=True),
    sa.Column('asp_connection', sa.String(), nullable=True),
    sa.Column('asp_connection_error', sa.String(), nullable=True),
    sa.Column('asp_custom_waveform_file_path_burst_a', sa.String(), nullable=True),
    sa.Column('asp_custom_waveform_file_path_burst_b', sa.String(), nullable=True),
    sa.Column('asp_custom_waveform_file_path_chirp_a', sa.String(), nullable=True),
    sa.Column('asp_custom_waveform_file_path_chirp_b', sa.String(), nullable=True),
    sa.Column('asp_status_summary', sa.String(), nullable=True),
    sa.Column('asp_trig_delay_burst_a', sa.Float(), nullable=True),
    sa.Column('asp_trig_delay_burst_a_override', sa.Integer(), nullable=True),
    sa.Column('asp_trig_delay_burst_a_use_override', sa.Integer(), nullable=True),
    sa.Column('asp_trig_delay_burst_b', sa.Float(), nullable=True),
    sa.Column('asp_trig_delay_burst_b_override', sa.Integer(), nullable=True),
    sa.Column('asp_trig_delay_burst_b_use_override', sa.Integer(), nullable=True),
    sa.Column('asp_trig_delay_chirp_a', sa.Float(), nullable=True),
    sa.Column('asp_trig_delay_chirp_a_override', sa.Integer(), nullable=True),
    sa.Column('asp_trig_delay_chirp_a_use_override', sa.Integer(), nullable=True),
    sa.Column('asp_trig_delay_chirp_b', sa.Float(), nullable=True),
    sa.Column('asp_trig_delay_chirp_b_override', sa.Integer(), nullable=True),
    sa.Column('asp_trig_delay_chirp_b_use_override', sa.Integer(), nullable=True),
    sa.Column('asp_unrecognized_firmware', sa.String(), nullable=True),
    sa.Column('asp_waveform_burst_a', sa.String(), nullable=True),
    sa.Column('asp_waveform_burst_b', sa.String(), nullable=True),
    sa.Column('asp_waveform_chirp_a', sa.String(), nullable=True),
    sa.Column('asp_waveform_chirp_b', sa.String(), nullable=True),
    sa.Column('attenuation_db_burst_a', sa.Integer(), nullable=True),
    sa.Column('attenuation_db_burst_b', sa.Integer(), nullable=True),
    sa.Column('attenuation_db_chirp_a', sa.Integer(), nullable=True),
    sa.Column('attenuation_db_chirp_b', sa.Integer(), nullable=True),
    sa.Column('auto_calculate_noise_regions', sa.Integer(), nullable=True),
    sa.Column('auto_calculate_signal_regions', sa.Integer(), nullable=True),
    sa.Column('bandwidth_burst_a', sa.Float(), nullable=True),
    sa.Column('bandwidth_burst_b', sa.Float(), nullable=True),
    sa.Column('bandwidth_chirp_a', sa.Float(), nullable=True),
    sa.Column('bandwidth_chirp_b', sa.Float(), nullable=True),
    sa.Column('cal_constant_burst_a_copol', sa.Float(), nullable=True),
    sa.Column('cal_constant_burst_a_crosspol', sa.Float(), nullable=True),
    sa.Column('cal_constant_burst_b_copol', sa.Float(), nullable=True),
    sa.Column('cal_constant_burst_b_crosspol', sa.Float(), nullable=True),
    sa.Column('cal_constant_chirp_a_copol', sa.Float(), nullable=True),
    sa.Column('cal_constant_chirp_a_crosspol', sa.Float(), nullable=True),
    sa.Column('cal_constant_chirp_b_copol', sa.Float(), nullable=True),
    sa.Column('cal_constant_chirp_b_crosspol', sa.Float(), nullable=True),
    sa.Column('cal_switch_enabled', sa.Integer(), nullable=True),
    sa.Column('cal_switch_enabled_effective', sa.Integer(), nullable=True),
    sa.Column('center_main_bang_burst_a', sa.Float(), nullable=True),
    sa.Column('center_main_bang_burst_b', sa.Float(), nullable=True),
    sa.Column('center_main_bang_chirp_a', sa.Float(), nullable=True),
    sa.Column('center_main_bang_chirp_b', sa.Float(), nullable=True),
    sa.Column('clutter_avg_len_a', sa.Integer(), nullable=True),
    sa.Column('clutter_avg_len_b', sa.Integer(), nullable=True),
    sa.Column('clutter_filter_enabled', sa.Integer(), nullable=True),
    sa.Column('coherent_on_recv_enabled', sa.Integer(), nullable=True),
    sa.Column('coherent_on_recv_gate_burst_a', sa.Integer(), nullable=True),
    sa.Column('coherent_on_recv_gate_burst_b', sa.Integer(), nullable=True),
    sa.Column('coherent_on_recv_gate_chirp_a', sa.Integer(), nullable=True),
    sa.Column('coherent_on_recv_gate_chirp_b', sa.Integer(), nullable=True),
    sa.Column('cold_noise_mw_burst_a_copol', sa.Float(), nullable=True),
    sa.Column('cold_noise_mw_burst_a_crosspol', sa.Float(), nullable=True),
    sa.Column('cold_noise_mw_burst_b_copol', sa.Float(), nullable=True),
    sa.Column('cold_noise_mw_burst_b_crosspol', sa.Float(), nullable=True),
    sa.Column('cold_noise_mw_chirp_a_copol', sa.Float(), nullable=True),
    sa.Column('cold_noise_mw_chirp_a_crosspol', sa.Float(), nullable=True),
    sa.Column('cold_noise_mw_chirp_b_copol', sa.Float(), nullable=True),
    sa.Column('cold_noise_mw_chirp_b_crosspol', sa.Float(), nullable=True),
    sa.Column('cold_noise_region_n_gates', sa.Integer(), nullable=True),
    sa.Column('cold_noise_region_n_gates_override', sa.Integer(), nullable=True),
    sa.Column('cold_noise_region_start_gate', sa.Integer(), nullable=True),
    sa.Column('cold_noise_region_start_gate_override', sa.Integer(), nullable=True),
    sa.Column('coolant_return_temp', sa.Float(), nullable=True),
    sa.Column('coolant_supply_temp', sa.Float(), nullable=True),
    sa.Column('data_trimming_enabled', sa.Integer(), nullable=True),
    sa.Column('digrcv_filter_bandwidth_ch1', sa.Float(), nullable=True),
    sa.Column('digrcv_filter_bandwidth_ch2', sa.Float(), nullable=True),
    sa.Column('digrcv_filter_bandwidth_ch3', sa.Float(), nullable=True),
    sa.Column('digrcv_filter_bandwidth_ch4', sa.Float(), nullable=True),
    sa.Column('digrcv_filter_bandwidth_effective_ch1', sa.Float(), nullable=True),
    sa.Column('digrcv_filter_bandwidth_effective_ch2', sa.Float(), nullable=True),
    sa.Column('digrcv_filter_bandwidth_effective_ch3', sa.Float(), nullable=True),
    sa.Column('digrcv_filter_bandwidth_effective_ch4', sa.Float(), nullable=True),
    sa.Column('digrcv_fir_dec', sa.Integer(), nullable=True),
    sa.Column('digrcv_fir_dec_effective', sa.Integer(), nullable=True),
    sa.Column('digrcv_fir_filter_delay', sa.Float(), nullable=True),
    sa.Column('eight_vdc', sa.Float(), nullable=True),
    sa.Column('eika_temp', sa.Float(), nullable=True),
    sa.Column('ems_1_override', sa.Integer(), nullable=True),
    sa.Column('ems_1_override_effective', sa.Integer(), nullable=True),
    sa.Column('ems_2_override', sa.Integer(), nullable=True),
    sa.Column('ems_2_override_effective', sa.Integer(), nullable=True),
    sa.Column('ems_delay', sa.Float(), nullable=True),
    sa.Column('ems_delay_override', sa.Float(), nullable=True),
    sa.Column('ems_delay_use_override', sa.Integer(), nullable=True),
    sa.Column('ems_use_override', sa.Integer(), nullable=True),
    sa.Column('ems_use_override_effective', sa.Integer(), nullable=True),
    sa.Column('fft_len_a', sa.Integer(), nullable=True),
    sa.Column('fft_len_b', sa.Integer(), nullable=True),
    sa.Column('fft_taper', sa.Integer(), nullable=True),
    sa.Column('fifteen_vdc', sa.Float(), nullable=True),
    sa.Column('five_point_two_vdc', sa.Float(), nullable=True),
    sa.Column('five_vdc', sa.Float(), nullable=True),
    sa.Column('group_b_enabled', sa.Integer(), nullable=True),
    sa.Column('group_b_enabled_effective', sa.Integer(), nullable=True),
    sa.Column('hot_noise_mw_burst_a_copol', sa.Float(), nullable=True),
    sa.Column('hot_noise_mw_burst_a_crosspol', sa.Float(), nullable=True),
    sa.Column('hot_noise_mw_burst_b_copol', sa.Float(), nullable=True),
    sa.Column('hot_noise_mw_burst_b_crosspol', sa.Float(), nullable=True),
    sa.Column('hot_noise_mw_chirp_a_copol', sa.Float(), nullable=True),
    sa.Column('hot_noise_mw_chirp_a_crosspol', sa.Float(), nullable=True),
    sa.Column('hot_noise_mw_chirp_b_copol', sa.Float(), nullable=True),
    sa.Column('hot_noise_mw_chirp_b_crosspol', sa.Float(), nullable=True),
    sa.Column('hot_noise_region_n_gates', sa.Integer(), nullable=True),
    sa.Column('hot_noise_region_n_gates_override', sa.Integer(), nullable=True),
    sa.Column('hot_noise_region_start_gate', sa.Integer(), nullable=True),
    sa.Column('hot_noise_region_start_gate_override', sa.Integer(), nullable=True),
    sa.Column('incl_pitch', sa.Float(), nullable=True),
    sa.Column('incl_roll', sa.Float(), nullable=True),
    sa.Column('lna_copol_temp', sa.Float(), nullable=True),
    sa.Column('lna_xpol_temp', sa.Float(), nullable=True),
    sa.Column('max_sampled_range_burst_a', sa.Float(), nullable=True),
    sa.Column('max_sampled_range_burst_b', sa.Float(), nullable=True),
    sa.Column('max_sampled_range_chirp_a', sa.Float(), nullable=True),
    sa.Column('max_sampled_range_chirp_b', sa.Float(), nullable=True),
    sa.Column('max_velocity_m_sec_burst_a', sa.Float(), nullable=True),
    sa.Column('max_velocity_m_sec_burst_b', sa.Float(), nullable=True),
    sa.Column('max_velocity_m_sec_chirp_a', sa.Float(), nullable=True),
    sa.Column('max_velocity_m_sec_chirp_b', sa.Float(), nullable=True),
    sa.Column('minus_five_vdc', sa.Float(), nullable=True),
    sa.Column('mod_blanked', sa.Integer(), nullable=True),
    sa.Column('mod_fault_time', sa.Float(), nullable=True),
    sa.Column('mod_has_fault', sa.Integer(), nullable=True),
    sa.Column('mod_high_voltage_on', sa.Integer(), nullable=True),
    sa.Column('mod_power_on', sa.Integer(), nullable=True),
    sa.Column('mod_transmitting', sa.Integer(), nullable=True),
    sa.Column('mod_warming_up', sa.Integer(), nullable=True),
    sa.Column('modulator_external_temp', sa.Float(), nullable=True),
    sa.Column('modulator_fault_interlock', sa.Integer(), nullable=True),
    sa.Column('modulator_fault_mod', sa.Integer(), nullable=True),
    sa.Column('modulator_fault_sum', sa.Integer(), nullable=True),
    sa.Column('modulator_fault_sync', sa.Integer(), nullable=True),
    sa.Column('modulator_fault_time_interlock', sa.Integer(), nullable=True),
    sa.Column('modulator_fault_time_mod', sa.Integer(), nullable=True),
    sa.Column('modulator_fault_time_sum', sa.Integer(), nullable=True),
    sa.Column('modulator_fault_time_sync', sa.Integer(), nullable=True),
    sa.Column('modulator_fault_time_transmitter_temp', sa.Integer(), nullable=True),
    sa.Column('modulator_fault_transmitter_temp', sa.Integer(), nullable=True),
    sa.Column('modulator_filament_delay', sa.Integer(), nullable=True),
    sa.Column('modulator_hv_on_command', sa.Integer(), nullable=True),
    sa.Column('modulator_power_on_command', sa.Integer(), nullable=True),
    sa.Column('modulator_power_valid', sa.Integer(), nullable=True),
    sa.Column('modulator_sync_divider', sa.Integer(), nullable=True),
    sa.Column('modulator_sync_enabled', sa.Integer(), nullable=True),
    sa.Column('modulator_sync_frequency', sa.Integer(), nullable=True),
    sa.Column('modulator_temp', sa.Float(), nullable=True),
    sa.Column('moments_fixed_roi_width_m_sec', sa.Integer(), nullable=True),
    sa.Column('moments_power_threshold_db', sa.Float(), nullable=True),
    sa.Column('moments_roi_mode', sa.Integer(), nullable=True),
    sa.Column('n_gates', sa.Integer(), nullable=True),
    sa.Column('n_gates_proc_burst_a', sa.Integer(), nullable=True),
    sa.Column('n_gates_proc_burst_b', sa.Integer(), nullable=True),
    sa.Column('n_gates_proc_chirp_a', sa.Integer(), nullable=True),
    sa.Column('n_gates_proc_chirp_b', sa.Integer(), nullable=True),
    sa.Column('n_group_pulses_a', sa.Integer(), nullable=True),
    sa.Column('n_group_pulses_b', sa.Integer(), nullable=True),
    sa.Column('noise_delay', sa.Float(), nullable=True),
    sa.Column('noise_delay_override', sa.Float(), nullable=True),
    sa.Column('noise_delay_use_override', sa.Integer(), nullable=True),
    sa.Column('noise_figure_db_burst_a_copol', sa.Float(), nullable=True),
    sa.Column('noise_figure_db_burst_a_crosspol', sa.Float(), nullable=True),
    sa.Column('noise_figure_db_burst_b_copol', sa.Float(), nullable=True),
    sa.Column('noise_figure_db_burst_b_crosspol', sa.Float(), nullable=True),
    sa.Column('noise_figure_db_chirp_a_copol', sa.Float(), nullable=True),
    sa.Column('noise_figure_db_chirp_a_crosspol', sa.Float(), nullable=True),
    sa.Column('noise_figure_db_chirp_b_copol', sa.Float(), nullable=True),
    sa.Column('noise_figure_db_chirp_b_crosspol', sa.Float(), nullable=True),
    sa.Column('noise_region_n_gates_nominal', sa.Integer(), nullable=True),
    sa.Column('noise_scale_factor_burst_a', sa.Float(), nullable=True),
    sa.Column('noise_scale_factor_burst_b', sa.Float(), nullable=True),
    sa.Column('noise_scale_factor_chirp_a', sa.Float(), nullable=True),
    sa.Column('noise_scale_factor_chirp_b', sa.Float(), nullable=True),
    sa.Column('noise_scale_factor_effective_burst_a', sa.Float(), nullable=True),
    sa.Column('noise_scale_factor_effective_burst_b', sa.Float(), nullable=True),
    sa.Column('noise_scale_factor_effective_chirp_a', sa.Float(), nullable=True),
    sa.Column('noise_scale_factor_effective_chirp_b', sa.Float(), nullable=True),
    sa.Column('noise_width', sa.Float(), nullable=True),
    sa.Column('noise_width_override', sa.Integer(), nullable=True),
    sa.Column('noise_width_use_override', sa.Integer(), nullable=True),
    sa.Column('outside_air_temp', sa.Float(), nullable=True),
    sa.Column('pentek_open', sa.String(), nullable=True),
    sa.Column('pentek_open_failed', sa.String(), nullable=True),
    sa.Column('pentek_receiving_data', sa.String(), nullable=True),
    sa.Column('pentek_run_failed', sa.String(), nullable=True),
    sa.Column('pentek_running', sa.String(), nullable=True),
    sa.Column('pentek_status_summary', sa.String(), nullable=True),
    sa.Column('plo1_lock_status', sa.Integer(), nullable=True),
    sa.Column('plo2_lock_status', sa.Integer(), nullable=True),
    sa.Column('plo3_lock_status', sa.Integer(), nullable=True),
    sa.Column('plo4_lock_status', sa.Integer(), nullable=True),
    sa.Column('post_avg_len', sa.Integer(), nullable=True),
    sa.Column('power_supply_temp', sa.Float(), nullable=True),
    sa.Column('pri_a', sa.Float(), nullable=True),
    sa.Column('pri_b', sa.Float(), nullable=True),
    sa.Column('pulse_compression_ratio_burst_a', sa.Float(), nullable=True),
    sa.Column('pulse_compression_ratio_burst_b', sa.Float(), nullable=True),
    sa.Column('pulse_compression_ratio_chirp_a', sa.Float(), nullable=True),
    sa.Column('pulse_compression_ratio_chirp_b', sa.Float(), nullable=True),
    sa.Column('pulse_compression_ratio_effective_burst_a', sa.Float(), nullable=True),
    sa.Column('pulse_compression_ratio_effective_burst_b', sa.Float(), nullable=True),
    sa.Column('pulse_compression_ratio_effective_chirp_a', sa.Float(), nullable=True),
    sa.Column('pulse_compression_ratio_effective_chirp_b', sa.Float(), nullable=True),
    sa.Column('range_gate_spacing', sa.Float(), nullable=True),
    sa.Column('range_gate_spacing_proc', sa.Float(), nullable=True),
    sa.Column('range_resolution_burst_a', sa.Float(), nullable=True),
    sa.Column('range_resolution_burst_b', sa.Float(), nullable=True),
    sa.Column('range_resolution_chirp_a', sa.Float(), nullable=True),
    sa.Column('range_resolution_chirp_b', sa.Float(), nullable=True),
    sa.Column('range_resolution_effective_burst_a', sa.Float(), nullable=True),
    sa.Column('range_resolution_effective_burst_b', sa.Float(), nullable=True),
    sa.Column('range_resolution_effective_chirp_a', sa.Float(), nullable=True),
    sa.Column('range_resolution_effective_chirp_b', sa.Float(), nullable=True),
    sa.Column('rcb_communication_error', sa.String(), nullable=True),
    sa.Column('rcb_connection', sa.String(), nullable=True),
    sa.Column('rcb_connection_error', sa.String(), nullable=True),
    sa.Column('rcb_humidity', sa.Float(), nullable=True),
    sa.Column('rcb_status_summary', sa.String(), nullable=True),
    sa.Column('rcb_status_valid', sa.Integer(), nullable=True),
    sa.Column('rcb_temp', sa.Float(), nullable=True),
    sa.Column('rcb_unrecognized_firmware', sa.String(), nullable=True),
    sa.Column('reverse_pwr_load_temp', sa.Float(), nullable=True),
    sa.Column('rf_unit_output_power_burst_a_dbm', sa.Float(), nullable=True),
    sa.Column('rf_unit_output_power_burst_b_dbm', sa.Float(), nullable=True),
    sa.Column('rf_unit_output_power_chirp_a_dbm', sa.Float(), nullable=True),
    sa.Column('rf_unit_output_power_chirp_b_dbm', sa.Float(), nullable=True),
    sa.Column('rf_unit_temp', sa.Float(), nullable=True),
    sa.Column('rtd14', sa.Float(), nullable=True),
    sa.Column('rtd15', sa.Float(), nullable=True),
    sa.Column('rtd16', sa.Float(), nullable=True),
    sa.Column('rtd6', sa.Float(), nullable=True),
    sa.Column('rtd7', sa.Float(), nullable=True),
    sa.Column('rtd8', sa.Float(), nullable=True),
    sa.Column('rx_gain_db_burst_a_copol', sa.Float(), nullable=True),
    sa.Column('rx_gain_db_burst_a_crosspol', sa.Float(), nullable=True),
    sa.Column('rx_gain_db_burst_b_copol', sa.Float(), nullable=True),
    sa.Column('rx_gain_db_burst_b_crosspol', sa.Float(), nullable=True),
    sa.Column('rx_gain_db_chirp_a_copol', sa.Float(), nullable=True),
    sa.Column('rx_gain_db_chirp_a_crosspol', sa.Float(), nullable=True),
    sa.Column('rx_gain_db_chirp_b_copol', sa.Float(), nullable=True),
    sa.Column('rx_gain_db_chirp_b_crosspol', sa.Float(), nullable=True),
    sa.Column('scope_communication_error', sa.String(), nullable=True),
    sa.Column('scope_connection', sa.String(), nullable=True),
    sa.Column('scope_connection_error', sa.String(), nullable=True),
    sa.Column('scope_lookup_table_missing', sa.String(), nullable=True),
    sa.Column('scope_status_summary', sa.String(), nullable=True),
    sa.Column('server_mode', sa.Integer(), nullable=True),
    sa.Column('server_state', sa.Integer(), nullable=True),
    sa.Column('signal_region_n_gates_a', sa.Integer(), nullable=True),
    sa.Column('signal_region_n_gates_a_override', sa.Integer(), nullable=True),
    sa.Column('signal_region_n_gates_b', sa.Integer(), nullable=True),
    sa.Column('signal_region_n_gates_b_override', sa.Integer(), nullable=True),
    sa.Column('signal_region_start_gate_a', sa.Integer(), nullable=True),
    sa.Column('signal_region_start_gate_a_override', sa.Integer(), nullable=True),
    sa.Column('signal_region_start_gate_b', sa.Integer(), nullable=True),
    sa.Column('signal_region_start_gate_b_override', sa.Integer(), nullable=True),
    sa.Column('sky_noise_mw_burst_a_copol', sa.Float(), nullable=True),
    sa.Column('sky_noise_mw_burst_a_crosspol', sa.Float(), nullable=True),
    sa.Column('sky_noise_mw_burst_b_copol', sa.Float(), nullable=True),
    sa.Column('sky_noise_mw_burst_b_crosspol', sa.Float(), nullable=True),
    sa.Column('sky_noise_mw_chirp_a_copol', sa.Float(), nullable=True),
    sa.Column('sky_noise_mw_chirp_a_crosspol', sa.Float(), nullable=True),
    sa.Column('sky_noise_mw_chirp_b_copol', sa.Float(), nullable=True),
    sa.Column('sky_noise_mw_chirp_b_crosspol', sa.Float(), nullable=True),
    sa.Column('sky_noise_region_n_gates', sa.Integer(), nullable=True),
    sa.Column('sky_noise_region_n_gates_override', sa.Integer(), nullable=True),
    sa.Column('sky_noise_region_start_gate', sa.Integer(), nullable=True),
    sa.Column('sky_noise_region_start_gate_override', sa.Integer(), nullable=True),
    sa.Column('software_dec', sa.Integer(), nullable=True),
    sa.Column('software_filter_burst_a', sa.String(), nullable=True),
    sa.Column('software_filter_burst_b', sa.String(), nullable=True),
    sa.Column('software_filter_chirp_a', sa.String(), nullable=True),
    sa.Column('software_filter_chirp_b', sa.String(), nullable=True),
    sa.Column('software_filter_file_path_burst_a', sa.String(), nullable=True),
    sa.Column('software_filter_file_path_burst_b', sa.String(), nullable=True),
    sa.Column('software_filter_file_path_chirp_a', sa.String(), nullable=True),
    sa.Column('software_filter_file_path_chirp_b', sa.String(), nullable=True),
    sa.Column('software_filter_output_trimming_power_threshold', sa.Float(), nullable=True),
    sa.Column('tukey_coef_burst_a', sa.Float(), nullable=True),
    sa.Column('tukey_coef_burst_b', sa.Float(), nullable=True),
    sa.Column('tukey_coef_chirp_a', sa.Float(), nullable=True),
    sa.Column('tukey_coef_chirp_b', sa.Float(), nullable=True),
    sa.Column('tukey_coef_effective_burst_a', sa.Float(), nullable=True),
    sa.Column('tukey_coef_effective_burst_b', sa.Float(), nullable=True),
    sa.Column('tukey_coef_effective_chirp_a', sa.Float(), nullable=True),
    sa.Column('tukey_coef_effective_chirp_b', sa.Float(), nullable=True),
    sa.Column('tukey_correction_burst_a', sa.Float(), nullable=True),
    sa.Column('tukey_correction_burst_b', sa.Float(), nullable=True),
    sa.Column('tukey_correction_chirp_a', sa.Float(), nullable=True),
    sa.Column('tukey_correction_chirp_b', sa.Float(), nullable=True),
    sa.Column('twelve_vdc', sa.Float(), nullable=True),
    sa.Column('twenty_eight_vdc', sa.Float(), nullable=True),
    sa.Column('tx_freq_burst', sa.Float(), nullable=True),
    sa.Column('tx_freq_chirp', sa.Float(), nullable=True),
    sa.Column('tx_pulse_bracketing', sa.Float(), nullable=True),
    sa.Column('tx_pulse_n_gates_burst_a', sa.Integer(), nullable=True),
    sa.Column('tx_pulse_n_gates_burst_b', sa.Integer(), nullable=True),
    sa.Column('tx_pulse_n_gates_chirp_a', sa.Integer(), nullable=True),
    sa.Column('tx_pulse_n_gates_chirp_b', sa.Integer(), nullable=True),
    sa.Column('tx_pulse_start_gate_burst_a', sa.Integer(), nullable=True),
    sa.Column('tx_pulse_start_gate_burst_b', sa.Integer(), nullable=True),
    sa.Column('tx_pulse_start_gate_chirp_a', sa.Integer(), nullable=True),
    sa.Column('tx_pulse_start_gate_chirp_b', sa.Integer(), nullable=True),
    sa.Column('tx_pulse_width_a', sa.Float(), nullable=True),
    sa.Column('tx_pulse_width_b', sa.Float(), nullable=True),
    sa.Column('tx_trigger_delay', sa.Float(), nullable=True),
    sa.Column('tx_trigger_enabled', sa.Integer(), nullable=True),
    sa.Column('tx_trigger_enabled_effective', sa.Integer(), nullable=True),
    sa.Column('use_digrcv_default_filter_ch1', sa.Integer(), nullable=True),
    sa.Column('use_digrcv_default_filter_ch2', sa.Integer(), nullable=True),
    sa.Column('use_digrcv_default_filter_ch3', sa.Integer(), nullable=True),
    sa.Column('use_digrcv_default_filter_ch4', sa.Integer(), nullable=True),
    sa.Column('use_digrcv_default_filter_effective_ch1', sa.Integer(), nullable=True),
    sa.Column('use_digrcv_default_filter_effective_ch2', sa.Integer(), nullable=True),
    sa.Column('use_digrcv_default_filter_effective_ch3', sa.Integer(), nullable=True),
    sa.Column('use_digrcv_default_filter_effective_ch4', sa.Integer(), nullable=True),
    sa.Column('use_software_filter_parameters', sa.Integer(), nullable=True),
    sa.Column('velocity_spacing_m_sec_burst_a', sa.Float(), nullable=True),
    sa.Column('velocity_spacing_m_sec_burst_b', sa.Float(), nullable=True),
    sa.Column('velocity_spacing_m_sec_chirp_a', sa.Float(), nullable=True),
    sa.Column('velocity_spacing_m_sec_chirp_b', sa.Float(), nullable=True),
    sa.Column('width_burst_a', sa.Float(), nullable=True),
    sa.Column('width_burst_b', sa.Float(), nullable=True),
    sa.Column('width_chirp_a', sa.Float(), nullable=True),
    sa.Column('width_chirp_b', sa.Float(), nullable=True),
    sa.Column('zero_gate_range_proc_burst_a', sa.Float(), nullable=True),
    sa.Column('zero_gate_range_proc_burst_b', sa.Float(), nullable=True),
    sa.Column('zero_gate_range_proc_chirp_a', sa.Float(), nullable=True),
    sa.Column('zero_gate_range_proc_chirp_b', sa.Float(), nullable=True),
    sa.Column('zero_gate_time', sa.Float(), nullable=True),
    sa.Column('zero_raw_gate_range_burst_a', sa.Float(), nullable=True),
    sa.Column('zero_raw_gate_range_burst_b', sa.Float(), nullable=True),
    sa.Column('zero_raw_gate_range_chirp_a', sa.Float(), nullable=True),
    sa.Column('zero_raw_gate_range_chirp_b', sa.Float(), nullable=True),
    sa.Column('zero_raw_gate_range_offset_burst_a', sa.Integer(), nullable=True),
    sa.Column('zero_raw_gate_range_offset_burst_b', sa.Integer(), nullable=True),
    sa.Column('zero_raw_gate_range_offset_chirp_a', sa.Integer(), nullable=True),
    sa.Column('zero_raw_gate_range_offset_chirp_b', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['instrument_id'], ['instruments.instrument_id'], ),
    sa.ForeignKeyConstraint(['site_id'], ['sites.site_id'], ),
    sa.PrimaryKeyConstraint('packet_id')]
    )
    op.create_table('pulse_captures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('instrument_id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('data', postgresql.ARRAY(sa.Float()), nullable=True),
    sa.ForeignKeyConstraint(['instrument_id'], ['instruments.instrument_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('table_references',
    sa.Column('instrument_id', sa.Integer(), nullable=False),
    sa.Column('referenced_tables', postgresql.ARRAY(sa.String()), nullable=True),
    sa.ForeignKeyConstraint(['instrument_id'], ['instruments.instrument_id'], ),
    sa.PrimaryKeyConstraint('instrument_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('table_references')
    op.drop_table('pulse_captures')
    op.drop_table('prosensing_paf')
    op.drop_table('instrument_logs')
    op.drop_table('instrument_data_references')
    op.drop_table('events_with_value')
    op.drop_table('events_with_text')
    op.drop_table('instruments')
    op.drop_table('users')
    op.drop_table('sites')
    op.drop_table('event_codes')
    ### end Alembic commands ###
