# PREDICCION F1

Esta es una aplicacion web para el registrar predicciones de carreras de F1, y asignar puntos segun se acierte o no en las mismas.

## Instalacion y test
1. Download and install google skd [https://cloud.google.com/sdk/docs](https://cloud.google.com/sdk/docs)
2. Install the components:

	gcloud components install app-engine-python
	gcloud components install app-engine-python-extras

3. Create a virtual environment (in python2)

	virtualenv -p /usr/bin/python2.7 predF1
	source predF1/bin/activate

4. Test locally:

	dev_appserver.py .
