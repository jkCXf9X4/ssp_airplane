within WingmanDrone;
model ControlInterface
  import GI = WingmanDrone.GeneratedInterfaces;
  parameter Real inputLag = 0.15;
  parameter Real manualCommandDefault(min=0.0, max=1.0) = 0.5;
  input GI.GenericElectricalBus powerIn;
  output GI.PilotCommand pilotCommandOut;
protected
  Real effectiveCommand;
equation
  effectiveCommand = (1 - inputLag) * manualCommandDefault + inputLag * min(1.0, max(0.0, powerIn.available_power_kw / 100.0));
  pilotCommandOut.stick_pitch_norm = min(1.0, max(-1.0, effectiveCommand - 0.5) * 2);
  pilotCommandOut.stick_roll_norm = 0.0;
  pilotCommandOut.rudder_norm = 0.0;
  pilotCommandOut.throttle_norm = min(1.0, max(0.0, effectiveCommand));
  pilotCommandOut.throttle_aux_norm = pilotCommandOut.throttle_norm;
  pilotCommandOut.button_mask = 0;
  pilotCommandOut.hat_x = 0;
  pilotCommandOut.hat_y = 0;
  pilotCommandOut.mode_switch = 0;
  pilotCommandOut.reserved = 0;
end ControlInterface;
