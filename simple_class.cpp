#include <iostream>
using namespace std;

class item{
	// this data is by default private
	int data;
	
	// class methods
	public:
	void set(int enter_value);
	int get_value(void);
};

void item::set(int enter_value){
	data = enter_value;
}

int item::get_value(void){
	return data;
}

int main(){
	item John, Joe, Sofie;
	
	John.set(5);
	Joe.set(6);
	Sofie.set(7);

	cout << "Data value for Sofie is " << Sofie.get_value() <<"\n";
	return 0;
}
