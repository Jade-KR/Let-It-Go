#include <Stepper.h>

// 1000 step ~== 3.6cm
#define QSize 30
#define nStep 10
#define boxNum 10
#define sensorswitch 600

int box_position[boxNum] = {0, 0, 200, 380, 560, 745, 745, 1500, 800, 900, };
Stepper myStepper(2048, 11, 9, 10, 8);
Stepper myStepper2(2048, 7, 5, 6, 4);
int cur_status = 0;
int cur_count = 0;
int chk_count = 3;
int prev_status = 0;

int Q_go_to_camera[QSize] = {0, };
int Q_go_to_camera_front=0;
int Q_go_to_camera_rear=0;
int Q_go_to_camera_distance = 4000;
int Q_go_to_check[QSize] = {0, };
int Q_go_to_check_front=0;
int Q_go_to_check_rear=0;
int Q_go_to_check_distance = 1000;

int Q_go_to_confirm[QSize] = {0, };
int Q_go_to_confirm_front=0;
int Q_go_to_confirm_rear=0;
int Q_go_to_confirm_distance = 2000;

int Q_go_to_box[QSize] = {0, };
int Q_go_to_box_front = 0;
int Q_go_to_box_rear = 0;
int box_status = 1;
int tmp;
int sensor;

char res;

void enQ(int Q[], int* rear, int val){
  tmp = (*rear - 1) % QSize;
  Q[*rear] = val - Q[tmp];
  *rear = *rear + 1;
  *rear = *rear % QSize;
  return;
}
void deQ(int* front){
  *front = *front + 1;
  *front = *front % QSize;
  return;
}
int chkQf(int front, int rear) {
  if (front == (rear + 1) % QSize) {
    return 1;
  }
  return 0;
}
int chkQe(int front, int rear) {
  if (front == rear) {
    return 1;
  }
  return 0;
}

void setup() {
  Serial.begin(9600);
  myStepper.setSpeed(10);
  myStepper2.setSpeed(10);
  box_status=1;
 // myStepper2.step(-30);
//  myStepper2.step(1000);
}


void loop() {
//   check sensor
  sensor = analogRead(A0);
  //Serial.println(sensor);
  
  
  if(sensor <= sensorswitch) cur_status = 1;
  else cur_status=0;
  if(cur_status != prev_status){
    cur_count++;
    if(cur_count>=chk_count){
      //change status
      prev_status = cur_status;
      cur_count = 0;
      // push value
      if(prev_status) {
        enQ(Q_go_to_camera, &Q_go_to_camera_rear, Q_go_to_camera_distance);
        //Serial.println("aaaaaaaaaaaaaaaaaaaaaaa");
      }
    }
  }
  else cur_count = 0;
  //Serial.println(Q_go_to_camera[Q_go_to_camera_front]);
  // check rasp res
  
//  if(Serial.available())Serial.println(Serial.read());
  
  // move
  
  myStepper.step(nStep);
  
  if (!chkQe(Q_go_to_camera_front, Q_go_to_camera_rear)){
    Q_go_to_camera[Q_go_to_camera_front] -= nStep;
    if (Q_go_to_camera[Q_go_to_camera_front] <= 0) {
      deQ(&Q_go_to_camera_front);
      delay(1000);
      Serial.write(1);
      enQ(Q_go_to_check, &Q_go_to_check_rear, Q_go_to_check_distance);
    }
  }
  
  if (!chkQe(Q_go_to_check_front, Q_go_to_check_rear)) {
    Q_go_to_check[Q_go_to_check_front] -= nStep;
    if (Q_go_to_check[Q_go_to_check_front] <= 0) {
      deQ(&Q_go_to_check_front);
      while(1){
        if (Serial.available()){
          res = Serial.read();
          if (res) {
            myStepper2.step(box_position[res] - box_position[box_status]);
            box_status = res;
          }
          
        //  Serial.println(res);
          //Serial.println(box_position[res] - box_position[box_status]);
          
          break;
        }
      }
      //enQ(Q_go_to_confirm, &Q_go_to_confirm_rear, Q_go_to_confirm_distance);
    }
  }
  /*
  if (!chkQe(Q_go_to_confirm_front, Q_go_to_confirm_rear)) {
    Q_go_to_confirm[Q_go_to_confirm_front] -= nStep;
    if (Q_go_to_confirm[Q_go_to_confirm_front] <= 0) {
      deQ(&Q_go_to_confirm_front);
    }
  }
  if (Q_go_to_confirm_front == Q_go_to_confirm_rear) {
    if (!chkQe(Q_go_to_box_front, Q_go_to_box_rear)) {
      if (Q_go_to_box[Q_go_to_box_front] > 0) {
        myStepper2.step(nStep);
        if (Q_go_to_box[Q_go_to_box_front] <= 0) {
          deQ(&Q_go_to_box_front);
        }
      }
      else {
        myStepper2.step(-nStep);
        if (Q_go_to_box[Q_go_to_box_front] >= 0) {
          deQ(&Q_go_to_box_front);
        }
      }
    }
  }
  else {
    if (Q_go_to_confirm_rear - Q_go_to_confirm_front == Q_go_to_box_rear - Q_go_to_box_front){
      myStepper2.step(Q_go_to_box[Q_go_to_box_front]);
      deQ(&Q_go_to_box_front);
    }
  }
  */
}
