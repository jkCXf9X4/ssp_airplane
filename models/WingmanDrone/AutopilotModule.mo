within WingmanDrone;
model AutopilotModule
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real updateRateHz = 25;
  parameter Real sensorFidelity = 0.95;
  Interfaces.RealInput feedbackBus;
  Interfaces.RealInput powerIn;
  Interfaces.RealOutput guidanceCmd;
protected
  Real stability;
equation
  stability = min(1.0, max(0.2, powerIn)) * sensorFidelity * feedbackBus;
  guidanceCmd = 0.5 * stability + 0.5 * feedbackBus;
end AutopilotModule;
