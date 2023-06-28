using System;
using System.Collections;

namespace Solution
{
    class MainClass
    {
        public static void Main(string[] args)
        {
            Stack stack = new Stack();
            stack.Push(1);
            stack.Push(1.1);
            stack.Push('z');
            stack.Push("Hello");

            foreach (var item in stack)
            {
                Console.WriteLine(item);
            }
        }
    }
    
}