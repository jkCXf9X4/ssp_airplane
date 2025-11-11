within WingmanDrone;
model ControlInterface
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real inputLag = 0.15;
  Interfaces.RealInput pilotCommand "0..1 manual command";
  Interfaces.RealInput powerIn;
  Interfaces.RealOutput pilotCommandOut;
protected
  Real effectiveCommand;
equation
  effectiveCommand = (1 - inputLag) * pilotCommand + inputLag * powerIn;
  pilotCommandOut = min(1.0, max(0.0, effectiveCommand));
end ControlInterface;
