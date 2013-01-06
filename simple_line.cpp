#include <iostream>
using namespace std;
 
// class, declaration part
class line
{
        char*  color;
        float  weight;
        float  length;
        char * arrow;
 
        public:
            line(void);
            char*    LineColor(char* color){return color;};
            float    LineWeight(float weight){return weight;};
            float    LineLength(float length){return length;};
            char    *LineArrow(char* arrow){return arrow = "YES";};
            ~line(void);
};
 
// implementation part
line::line(void)
{
        // constructors or default initial values.
        weight = 0.25;
        length = 10;
}
 
line::~line(void)
{
        color = NULL;
        weight = 0;
        length = 0;
        arrow = NULL;
}
 
// main program
int main()
{
        line   LineOne;
 
        float x = 1.25, y = 2.25;
        char newcolor[10] = "BLUE", *colorptr;
 
        cout<<"Line attributes, very simple\n";
        cout<<"     class example\n";
        cout<<"----------------------------"<<"\n";
 
        colorptr = newcolor;
        // just for testing the new attribute values...
        cout<<"\nAs normal variables....."<<endl;
        cout<<"Test the new line weight = "<<x<<endl;
        cout<<"Test the new line length = "<<y<<endl;
        cout<<"Test the new line color is = "<<colorptr<<endl;
 
        cout<<"\nUsing class......."<<endl;
        cout<<"New line's color  ----> "<<LineOne.LineColor(colorptr)<<"\n";
        cout<<"New line's weight ----> "<<LineOne.LineWeight(x)<<" unit"<<"\n";
        cout<<"New line's length ----> "<<LineOne.LineLength(y)<<" unit""\n";
        cout<<"Line's arrow      ----> "<<LineOne.LineArrow(" ")<<"\n\n";
        return 0;
}
