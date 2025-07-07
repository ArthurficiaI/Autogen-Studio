First install Autogen Studio:

pip install -U autogenstudio

To start the application use the following command:

autogenstudio ui --appdir .\autogen_studio_data --port 8086

In the official example they use port 8081 but that port is probably taken if you're trying to run some testcases.


Navigate to Playground to try the ASE_Team out.
To use it, simply ask for the repository number you want to try out. Like this: "Do case x"
![image](https://github.com/user-attachments/assets/f69fd82d-3d3a-4352-9619-1cf80856eb84)


If you want to take a look at the code, you can simply navigate to the Team Builder.
There you can enable seeing the whole json by disabling the visual builder switch, otherwise you can also click on the agents to see their code!
![image](https://github.com/user-attachments/assets/6f758301-f61e-4905-83ec-cc522304d89b)

If you want to explicitly see if the changes were successful you can execute run-tests.py for the results, although the agents are testing themselves and will write their results in a file called agentTestResults.log



