void setup() {
  Serial.begin(9600);
}

void loop() {
  String message = "";
  while (Serial.available())
    message.concat((char) Serial.read());
  if (message != "")
    Serial.println(message);
}
