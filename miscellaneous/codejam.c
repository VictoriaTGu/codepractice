int main (int argc, char *argv[]){
  char *infile = argv[1];
  char *outfile = argv[2];
  
  FILE *inptr = fopen(infile, "r");
  FILE *outptr = fopen(outfile, "w");
  
  int cases;
  fread(&cases, sizeof(int), 1, inptr);
  
  while(cases>0){
    fread(&numplayers, sizeof(int), 1, inptr)
    int array[numplayers+1];
    fread(array, sizeof(int), numplayers, inptr);

    int tempnum = numplayers;
    int sum = 0;
    int total = 0;
    int largest = 0;

    int n;
    for(int n=0;n<numplayers;n++){
	  if (array[n]>largest)
	    {
	      largest=array[n];
	    }
	  total+=array[n];
	}
  
    int difference=largest;
  
      while(tempnum >0){
          int i;
          for(int i=0;i<numplayers;i++)
            {
	      int j;
              for(int j=(i+1); j<numplayers;n++)
                {
		  int k;
                  for(int k=(j+1);k<numplayers;k++)
		    {
		      int l;
                      for(int l=(k+1);l<numplayers;l++)
			{
                          int tempsum = array[i]+array[j]+array[k]+array[l];
                          int other= total-tempsum;
                          int tempdiff = abs(other-tempsum);
                          if(tempdiff < difference)
			    difference = tempdiff;
			}
		    }
                }
            }
            
	  tempnum-=2;
	}

    }
      
  cases-=1;
}
  
