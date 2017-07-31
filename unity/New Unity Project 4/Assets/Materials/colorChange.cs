using UnityEngine;
using System.Collections;

public class colorChange : MonoBehaviour {

	int touchCount;
	int maxColorCount;
	int currentColor;
	Material material;
	public Color[] colors;

	void Awake()
	{
		touchCount = 0;
		maxColorCount = 3;
		currentColor = 0;
		material = GetComponent<MeshRenderer>().material;
		material.color = colors[currentColor];

		StartCoroutine("colorFunc");
		StartCoroutine("colorFunc2");
	}

	IEnumerator colorFunc()
	{
		while (true)
		{
			yield return null;

			this.touchCount = Input.touchCount;

			if (this.touchCount > 0)
			{
				if (Input.GetTouch(0).phase == TouchPhase.Began)
				{
					currentColor++;
					if (currentColor >= maxColorCount) currentColor = 0;

					material.color = colors[currentColor];
				}
			}
		}
	}

	IEnumerator colorFunc2()
	{
		while (true)
		{
			yield return null;

			if (Input.GetMouseButtonDown(0))
			{
				currentColor++;
				if (currentColor >= maxColorCount) currentColor = 0;

				material.color = colors[currentColor];
			}
		}
	}
}
	