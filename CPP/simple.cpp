#include <iostream>
using namespace std;

struct item{
	int data;
};

int main(){
	item John, Joe, Sofie;
	int Pika;
	
	John.data = 5;
	Joe.data = 6;
	Sofie.data = 7;
	Pika = 8;

	cout << "Data value for John is " << John.data <<"\n";
	return 0;
}
