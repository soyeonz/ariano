#pragma strict

var Btn_Start_Text : UI.Text;
var Time_Count : float;

function BtnRestart () {
    UnityEngine.SceneManagement.SceneManager.LoadScene("00_Main") ;
}

function Update () {
	Time_Count += Time.deltaTime;
	if(Time_Count > 1.8) Time_Count = 0;
	
	if (Time_Count < 0.9)	Btn_Start_Text.color = Color(0,0,0,(1-Time_Count));
	else					Btn_Start_Text.color = Color(0,0,0,(Time_Count-0.8));
}