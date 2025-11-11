within SSPAirplane;
model MotorArray
  parameter Integer count(min=1) = 4;
  parameter Real thrustPerMotor_kN = 120;
  parameter Real motorEfficiency(min=0, max=1) = 0.9;
  parameter Real motorPowerScale(min=0.5, max=1.5) = 1.0;
  parameter Real powerPerThrust = 0.04 "MW required per kN baseline";
  Modelica.Blocks.Interfaces.RealInput electricalPowerMW;
  Modelica.Blocks.Interfaces.RealInput throttleCmd;
  Modelica.Blocks.Interfaces.RealOutput thrust_kN;
  Modelica.Blocks.Interfaces.RealOutput powerDrawMW;
protected
  parameter Real maxPowerMW = count * thrustPerMotor_kN * powerPerThrust * motorPowerScale / motorEfficiency;
  Real commandedPowerMW;
equation
  commandedPowerMW = min(maxPowerMW * max(0, throttleCmd), electricalPowerMW);
  powerDrawMW = commandedPowerMW;
  thrust_kN = motorEfficiency * powerDrawMW / powerPerThrust;
end MotorArray;
