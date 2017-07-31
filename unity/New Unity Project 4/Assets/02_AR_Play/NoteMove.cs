using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NoteMove : MonoBehaviour {

	public int Speed;
	public float moveFloat;
	public Vector3 currentPosition = new Vector3(-1,1,0);
	public Vector3 TargetPosition = new Vector3(-1,0,0);

	void Awake() {
		//StartCoroutine ("speedFunc");
	}
	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		float fMove = Time.deltaTime * Speed;
		//transform.Translate (Vector3.down * fMove);
		this.transform.position = Vector3.MoveTowards(currentPosition,TargetPosition,fMove);
	}

	IEnumerator speedFunc()
	{
		while (true)
		{
			yield return null;

			if (Input.GetMouseButtonDown(0))
			{
				Debug.Log ("whyyyyyyyyyyyy");
				transform.Translate (Vector3.back * Speed * Time.deltaTime);
			}
		}
	}
}
