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
  Interfaces.RealOutput orientationDeg;
  Interfaces.RealOutput locationKm;
protected
  Real blendCmd;
  Real powerFactor;
  Real headingDeg(start=0);
  Real positionKm(start=0);
  parameter Real headingGain = 60;
  parameter Real velocityGain = 180;
equation
  blendCmd = 0.6 * autonomyPort + 0.4 * manualInput;
  powerFactor = min(1.0, max(0.2, powerIn));
  engineThrottle = min(1.0, max(0.1, blendCmd * powerFactor));
  surfaceBus = min(1.0, engineThrottle + 0.1 * powerFactor);
  flightStatus = 0.4 * engineThrottle + 0.4 * surfaceBus + 0.2 * (orientationDeg / 360);
  der(headingDeg) = headingGain * (manualInput - 0.5) + 20 * (autonomyPort - 0.5);
  der(positionKm) = velocityGain * engineThrottle;
  orientationDeg = headingDeg;
  locationKm = positionKm;
end MissionComputer;
