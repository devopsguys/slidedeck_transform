if(-Not(Get-Command "npm" -ErrorAction SilentlyContinue))
{
    throw "NodeJS is not installed. It is required in order to run this application."
}

if(-Not(Get-Command "python" -ErrorAction SilentlyContinue))
{
    throw "Python is not installed. It is required in order to run this application."
}

pip install -r slidedeck_transform/requirements.txt
npm install
npm start