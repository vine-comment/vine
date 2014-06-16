if [ "$(uname)" == "Darwin" ]; then
  sh mac-install.sh
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  sh ubuntu-install.sh
else
  echo "Unsupport OS $(uname -s)"
fi
