within SSPAirplane;
model ControlSoftware
  parameter Real redundancyLevel = 3;
  parameter Real computeBudgetTOPS = 30;
  Modelica.Blocks.Interfaces.RealInput guidanceCommand "0..1 long range guidance";
  Modelica.Blocks.Interfaces.RealInput payloadCapacityKg;
  Modelica.Blocks.Interfaces.RealInput avionicsPowerMW;
  Modelica.Blocks.Interfaces.RealOutput throttleCmd;
  Modelica.Blocks.Interfaces.RealOutput liftCommand;
protected
  Real payloadBias;
equation
  payloadBias = min(0.2, payloadCapacityKg / 100000);
  throttleCmd = min(1.0, max(0.2, guidanceCommand + payloadBias));
  liftCommand = min(1.0, throttleCmd + avionicsPowerMW * 0.05);
end ControlSoftware;
