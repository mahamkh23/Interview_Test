## Prerequisites
1.Ensure that both Python and Appium are installed and properly set up on your system.

2.Download the appropriate version of ChromeDriver that matches your Android device. After downloading, place the `chromedriver.exe` file in the Appium directory.

3. Update your capabilities as follows:


CAPS=

{
   
	"platformName": "Android",
    "browserName": "Chrome",
    "appium:options": {
    "platformVersion": "13",  # Change this to your device version
    "deviceName": "RF8T40T905V",  # Change this to your device name
    "automationName": "UiAutomator2",
    "chromedriverVersion": "your_chromedriver_version",  # specify your ChromeDriver version
    "chromedriverExecutableDir": r"C:\path\to\chromedriver.exe"  # path to the chromedriver
    }
}

5.Launch the Appium server using the command line.

6.Execute your test script in the PyCharm IDE.
## Important
Ensure that the Appium server is running before you start your tests. If you experience any issues with device connectivity, just verify your USB connection and device settings.
