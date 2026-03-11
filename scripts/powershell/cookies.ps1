docker stop chromium

$SELENIUM_IMAGE = "selenium/standalone-chromium"

docker run --rm --name chromium -d -p 4444:4444 -p 7900:7900 --shm-size="2g" $SELENIUM_IMAGE

Write-Host "Waiting for Selenium server to be ready..."

$URL = "http://localhost:4444/status"
do  {
	Start-Sleep -Seconds 1
	Write-Host "loading..."
	$response = try {
		Invoke-RestMethod -Uri $URL -UseBasicParsing
	} catch {
		$null
	}
} while (-not ($response.value.ready -eq $true))

docker run --rm -it --mount type=bind,source=.,destination=/ja_api nauseousspartan/ja_api sign_in auth

docker stop chromium
