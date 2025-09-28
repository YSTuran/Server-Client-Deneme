#include <iostream>

using namespace std;

class calculations
{
public:
  int x, y;

  void addition()
  {
    cout << "Insert the first value: ";
    cin >> x;
    cout << "Insert the second value: ";
    cin >> y;

    cout << "The result of the operation: " << x + y << "\n";
  }
  void subtraction()
  {
    cout << "Insert the first value: ";
    cin >> x;
    cout << "Insert the second value: ";
    cin >> y;

    cout << "The result of the operation: " << x - y << "\n";
  }
  void multiplication()
  {
    cout << "Insert the first value: ";
    cin >> x;
    cout << "Insert the second value: ";
    cin >> y;

    cout << "The result of the operation: " << x * y << "\n";
  }
  void divide()
  {
    float i, j;
    cout << "Insert the first value: ";
    cin >> i;
    cout << "Insert the second value: ";
    cin >> j;

    cout << "The result of the operation: " << i / j << "\n";
  }
  void menuScript()
  {
    cout << "Hello welcome to the calculator. Press Y to countinue, N to exit the program. ";
  }
  void operations()
  {
    cout << "Press 1 to addition, 2 to subtract, 3 to multiply, 4 to divide, 5 to return to the main menu and 6 to exit the program. \n";
  }
  void exitMessage()
  {
    cout << "You are leaving the program. I hope you enjoyed the program. See you again. ";
  }
  void alert()
  {
    cout << "Please try again \n";
  }
};
int main()
{

  calculations xdxd;

  char a;

 
    k1: xdxd.menuScript();
    cin>>a;

    if(a=='Y'){
     k2: xdxd.operations();
     int b;
     cin>>b;
     switch (b)
     {
      case 1:
       xdxd.addition();
       goto k2;
      case 2:
      xdxd.subtraction();
       goto k2;  
      case 3:
       xdxd.multiplication();
       goto k2;
      case 4:
       xdxd.divide();
       goto k2;
      case 5:
       goto k1;
      case 6:
       xdxd.exitMessage();
       break;
      default:
       xdxd.alert();
       goto k2;  
     }
    }
    else if(a=='N'){
     xdxd.exitMessage();
    
    }
    else{
     xdxd.alert();
     goto k1;
    }
  

  return 0;
}
