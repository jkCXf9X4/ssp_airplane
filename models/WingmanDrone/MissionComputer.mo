within WingmanDrone;
model MissionComputer
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real redundancyLevel = 3;
  parameter Real computeBudgetTOPS = 25;
  Interfaces.RealInput manualInput;
  Interfaces.RealInput autonomyPort;
  Interfaces.RealInput powerIn;
  Interfaces.RealOutput engineThrottle;
  Interfaces.RealOutput surfaceBus;
  Interfaces.RealOutput flightStatus;
protected
  Real blendCmd;
  Real powerFactor;
equation
  blendCmd = 0.6 * autonomyPort + 0.4 * manualInput;
  powerFactor = min(1.0, max(0.2, powerIn));
  engineThrottle = min(1.0, max(0.1, blendCmd * powerFactor));
  surfaceBus = min(1.0, engineThrottle + 0.1 * powerFactor);
  flightStatus = 0.5 * engineThrottle + 0.5 * surfaceBus;
end MissionComputer;
