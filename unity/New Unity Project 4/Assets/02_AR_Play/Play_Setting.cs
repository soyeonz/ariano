using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.VR;

public class Play_Setting : MonoBehaviour {

	// Use this for initialization
	void Start () {
		StartCoroutine (LoadDevice ("cardboard"));
	}

	IEnumerator LoadDevice(string newDevice)
	{
		VRSettings.LoadDeviceByName(newDevice);
		yield return null;
		VRSettings.enabled = true;
	}
}
