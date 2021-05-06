using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WBFCommuncation
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

#pragma warning disable IDE0044 // Add readonly modifier

        Process myProcess = new Process();
        StreamWriter myStreamWriter;
        StreamReader myStreamReader;
        SerialPort sp = new SerialPort("COM7", 9600);

        Dictionary<string, Vector> boardPositions = new Dictionary<string, Vector>();
        private List<string> alreadyMadeMoves = new List<string>();

#pragma warning restore IDE0044 // Add readonly modifier

        const double numberOfFieldsInRow = 8;
        readonly double LengthOfBoardField = 3;

        const double lengthToFirstJoint = 8;
        const double lengthToSecondJoint = 13;
        const double lengthToEndEffector = 12.5;

        const double a1 = 8;
        const double a2 = 13;
        const double a3 = 12.5;

        double rotateAngle = -1;
        double firstJointAngle = -1;
        double secondJointAngle = -1;

        private bool startNewGame = true;

        public MainWindow()
        {
            InitializeComponent();
            InitializeBoard();

            myProcess.StartInfo.FileName = "stockfish_x86-64-bmi2.exe";
            myProcess.StartInfo.UseShellExecute = false;
            myProcess.StartInfo.RedirectStandardInput = true;
            myProcess.StartInfo.RedirectStandardOutput = true;
            myProcess.StartInfo.CreateNoWindow = true;

            myProcess.Start();

            myStreamWriter = myProcess.StandardInput;
            myStreamReader = myProcess.StandardOutput;

        }

        private void buttonOn_Click(object sender, RoutedEventArgs e)
        {
            MoveRobotArm(); 
        }

        private void ComputerMove_Click(object sender, RoutedEventArgs e)
        {
            MakeMove(ComputerMakesMove());
        }

        private void HumanMove_Click(object sender, RoutedEventArgs e)
        {
            string humanMove = FromTextBox.Text + ToTextBox.Text ;
            MakeMove(humanMove);
        }

        #region Chess move

        private void MakeMove(string FromToField)
        {
            if (startNewGame == true)
            {
                InitializeGame();
                startNewGame = false;
            }

            alreadyMadeMoves.Add(FromToField);
            string fromField = alreadyMadeMoves.Last().Substring(0, 2);
            string toField = alreadyMadeMoves.Last().Substring(2);

            MoveRobotArm(fromField);
            Thread.Sleep(4000);
            MoveRobotArm(toField);
            Thread.Sleep(4000);

            string textBoxContent = "";

            foreach (string move in alreadyMadeMoves)
            {
                textBoxContent += move + Environment.NewLine;
            }

            textBox.Text = textBoxContent;
        }

        private String ComputerMakesMove()
        {
            string positionFromEngine = "position startpos moves";

            foreach (string move in alreadyMadeMoves)
            {
                positionFromEngine += " " + move;
            }

            myStreamWriter.WriteLine(positionFromEngine);
            Thread.Sleep(500);

            myStreamWriter.WriteLine("go depth 5");
            Console.WriteLine("go depth 5");
            Thread.Sleep(2000);

            string kek;

            do
            {
                kek = myStreamReader.ReadLine();
            } while (!kek.Contains("kupa"));

            string[] megakeka = kek.Split(' ');

            return megakeka[1];
        }

        private void InitializeGame()
        {
            myStreamWriter.WriteLine("uci");
            Console.WriteLine("uci");
            Thread.Sleep(1000);

            myStreamWriter.WriteLine("ucinewgame");
            Console.WriteLine("ucinewgame");
            Thread.Sleep(500);

            myStreamWriter.WriteLine("position startpos");
            Console.WriteLine("position startpos");
            Thread.Sleep(500);
        }

        private void InitializeBoard()
        {

            for (int i = 0; i < numberOfFieldsInRow; i++)
            {
                for (int j = 97; j < 97 + numberOfFieldsInRow; j++)
                {
                    double x = ((LengthOfBoardField * numberOfFieldsInRow / 2) - (LengthOfBoardField / 2)) - (j - 97)
                        * (((LengthOfBoardField * numberOfFieldsInRow) / 2) / (numberOfFieldsInRow / 2));
                    double y = (i + 1) * LengthOfBoardField - (LengthOfBoardField / 2);

                    string nazwaPola = ((char)j).ToString() + (i + 1);

                    boardPositions.Add(nazwaPola, new Vector(x, y));


                }
            }
        } 

        #endregion

        #region Arm controlling functions

        private void MoveRobotArm()
        {
            InverseKinematics3(int.Parse(xaxis.Text), int.Parse(yaxis.Text), int.Parse(zaxis.Text));

            Bounding();

            try
            {
                writed.Text = rotateAngle + "s" + firstJointAngle + "s" + secondJointAngle + "\n";
                sp.Write(rotateAngle + "s" + firstJointAngle + "s" + secondJointAngle + "\n");

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private void MoveRobotArm(string toField)
        {
            Vector moveCoordinates = boardPositions.First(x => x.Key == toField).Value;
            InverseKinematics3(moveCoordinates.X, moveCoordinates.Y, 0.2 );

            Bounding();

            writed.Text = rotateAngle + "s" + firstJointAngle + "s" + secondJointAngle + "\n";
            sp.Write(rotateAngle + "s" + firstJointAngle + "s" + secondJointAngle + "\n");
        }

        private void Bounding()
        {
            rotateAngle = 90 - rotateAngle;

            firstJointAngle += 65;                  // can be max 115

            secondJointAngle = 178 + secondJointAngle;

            rotateAngle = Math.Round(rotateAngle);
            firstJointAngle = Math.Round(firstJointAngle);
            secondJointAngle = Math.Round(secondJointAngle);

            theta1.Text = rotateAngle.ToString();
            theta2.Text = firstJointAngle.ToString();
            theta3.Text = secondJointAngle.ToString();
        }

        private void InverseKinematics3(double x, double y, double z)
        {
            double r = Math.Sqrt(Math.Pow(x, 2) + Math.Pow(y, 2));

            secondJointAngle = -Math.Acos((Math.Pow(r, 2) + Math.Pow(z - a1, 2) - Math.Pow(a2, 2) - Math.Pow(a3, 2)) / (2 * a2 * a3));
            firstJointAngle = Math.Atan2(z - a1, r) - Math.Atan2(a3 * Math.Sin(secondJointAngle), a2 + a3 * Math.Cos(secondJointAngle));
            rotateAngle = Math.Atan2(x, y);

            rotateAngle = ConvertRadiansToDegrees(rotateAngle);
            secondJointAngle = ConvertRadiansToDegrees(secondJointAngle);
            firstJointAngle = ConvertRadiansToDegrees(firstJointAngle);

        }

        private void InverseKinematics2(double x, double y, double z)
        {
            rotateAngle = Math.Atan(y / x);

            secondJointAngle = Math.Acos((Math.Pow(x, 2) + Math.Pow(y, 2) + Math.Pow(z - a1, 2) - Math.Pow(a2, 2) - Math.Pow(a3, 2)) / (2 * a2 * a3));

            firstJointAngle = Math.Atan(
                (
                    (z - a1) *
                    (
                        a2 + a3 * Math.Cos(secondJointAngle) - Math.Sqrt
                        (
                            Math.Pow(x, 2) + Math.Pow(y, 2)
                        )
                        * a3 * Math.Sin(secondJointAngle)
                    )
                )
                /
                (
                    Math.Sqrt(
                        Math.Pow(x, 2) + Math.Pow(y, 2)
                        )
                    *
                    (
                        a2 + a3 * Math.Cos(secondJointAngle)
                    )
                    + (z - a1) * a3 * Math.Sin(secondJointAngle)
                )
            );


            rotateAngle = ConvertRadiansToDegrees(rotateAngle);
            secondJointAngle = ConvertRadiansToDegrees(secondJointAngle);
            firstJointAngle = ConvertRadiansToDegrees(firstJointAngle);

        }

        private void InverseKinematics(double x, double y, double z)
        {
            rotateAngle = Math.Atan(y / x);
            rotateAngle = ConvertRadiansToDegrees(rotateAngle);

            double r1 = Math.Sqrt(Math.Pow(x, 2) + Math.Pow(y, 2));
            double r2 = z - lengthToFirstJoint;
            double tempAngle2 = Math.Atan(r2 / r1);
            double r3 = Math.Sqrt(Math.Pow(r1, 2) + Math.Pow(r2, 2));
            double tempAngle1 = Math.Acos(
                (Math.Pow(lengthToEndEffector, 2) - Math.Pow(lengthToSecondJoint, 2) - Math.Pow(r3, 2))
                / (-2 * lengthToSecondJoint * r3)
                );
            firstJointAngle = ConvertRadiansToDegrees(tempAngle2) - ConvertRadiansToDegrees(tempAngle1);
            firstJointAngle = 90 - firstJointAngle;

            double tempAngle3 = Math.Acos(
                (Math.Pow(r3, 2) - Math.Pow(lengthToSecondJoint, 2) - Math.Pow(lengthToEndEffector, 2))
                / (-2 * lengthToSecondJoint * lengthToEndEffector)
                );
            secondJointAngle = -(180 - ConvertRadiansToDegrees(tempAngle3));
        }

        public double ConvertRadiansToDegrees(double radians)
        {
            double degrees = (180 / Math.PI) * radians;
            return (degrees);
        }

        #endregion

        #region Some other functions

        private void buttonPortOpen_Click(object sender, RoutedEventArgs e)
        {
            sp.Open();
            checkBox.IsChecked = true;
        }

        private void buttonPortClose_Click(object sender, RoutedEventArgs e)
        {
            sp.Close();
            checkBox.IsChecked = false;
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            myProcess.Close();
        }

        #endregion
    }
}
