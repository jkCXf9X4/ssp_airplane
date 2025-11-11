within SSPAirplane;
model ControlSoftware
  import Interfaces = SSPAirplane.Interfaces;
  parameter Real redundancyLevel = 3;
  parameter Real computeBudgetTOPS = 30;
  Interfaces.RealInput guidanceCommand "0..1 long range guidance";
  Interfaces.RealInput payloadCapacityKg;
  Interfaces.RealInput avionicsPowerMW;
  Interfaces.RealOutput throttleCmd;
  Interfaces.RealOutput liftCommand;
protected
  Real payloadBias;
equation
  payloadBias = min(0.2, payloadCapacityKg / 100000);
  throttleCmd = min(1.0, max(0.2, guidanceCommand + payloadBias));
  liftCommand = min(1.0, throttleCmd + avionicsPowerMW * 0.05);
end ControlSoftware;
