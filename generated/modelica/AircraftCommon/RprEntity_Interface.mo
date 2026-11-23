within AircraftCommon;

partial model RprEntity_Interface
  parameter String transport = "loopback";
  parameter String bind_address = "127.0.0.1:5000";
  parameter String peer_address = "";
  input GeneratedInterfaces.EntityState entityState;
  output GeneratedInterfaces.EntityState peerState;
end RprEntity_Interface;
