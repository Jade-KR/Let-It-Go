#include <Stepper.h>

// 2048:한바퀴(360도), 1024:반바퀴(180도)...
const int stepsPerRevolution = 2048; 
// 모터 드라이브에 연결된 핀 IN4, IN2, IN3, IN1
Stepper myStepper(stepsPerRevolution,11,9,10,8);
int Light;

int cnt = 0;       
void setup() {
  myStepper.setSpeed(18); 
  Serial.begin(9600);
  pinMode(7, OUTPUT);
}
void loop() {
//  digitalWrite(7, HIGH);
//  delay(1000);
//  digitalWrite(7, LOW);
//  delay(1000);
  // 시계 반대 방향으로 한바퀴 회전
  delay(1000);
  Light = analogRead(A0);
//  myStepper.step(stepsPerRevolution);
//  delay(500);
  Serial.println(Light);
//  Serial.println(cnt++);
//
//  // 시계 방향으로 한바퀴 회전
//  myStepper.step(-stepsPerRevolution);
//  myStepper.setSpeed(28); 
//  Serial.println(cnt);
//  cnt += 1;
//  delay(500);
}
