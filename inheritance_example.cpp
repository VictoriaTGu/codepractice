#include <iostream>
using namespace std;

class vehicle{
	// protected means it would be accessible to derived classes
	private:
		int wheels;
		float weight;
	public:
		void initialize(int input_wheels, float input_weight);
		int get_wheels(void);
		float get_weight(void);	
		float wheel_load(void);
};

// The car class inherits from vehicle
class car: public vehicle{
	int passenger_load;
	public:
		void initialize(int input_wheels, float input_weight, int people=4);
		int passengers(void){
			return passenger_load;
		}
};

// this method overrides the base class' initialize function
void car::initialize(int input_wheels, float input_weight, int people){
	passenger_load = people;
	//weight = input_weight;
	//wheels = input_wheels;

	// the data is not directly available, so must send message
	//	to the message in the base class
	vehicle::initialize(input_wheels, input_weight);
}

void vehicle::initialize(int input_wheels, float input_weight){
	wheels = input_wheels;
	weight = input_weight;
}

int vehicle::get_wheels(void){
	return wheels;
}

float vehicle::get_weight(void){
	return weight;
}

float vehicle::wheel_load(void){
	return (weight / wheels);
}

int main(void){
	car sedan;
	sedan.initialize(3, 8.0, 4);
	cout << "Wheel load: " << sedan.wheel_load() <<"\n";
	cout << "Passengers: " << sedan.passengers() <<"\n";
}
