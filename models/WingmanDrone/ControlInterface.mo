within WingmanDrone;
model ControlInterface
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real inputLag = 0.15;
  parameter Real manualCommandDefault(min=0.0, max=1.0) = 0.5;
  Interfaces.RealInput powerIn;
  Interfaces.RealOutput pilotCommandOut;
protected
  Real effectiveCommand;
equation
  effectiveCommand = (1 - inputLag) * manualCommandDefault + inputLag * powerIn;
  pilotCommandOut = min(1.0, max(0.0, effectiveCommand));
end ControlInterface;
