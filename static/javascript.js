
  const weatherWidget = document.querySelector(".weather-widget-container");
  const cityName = document.querySelector(".city");
  const temperature = document.querySelector(".temperature");
  const weatherIcon = document.querySelector(".weathericon");
  const description = document.querySelector(".description");
  let lastSrc = weatherIcon.getAttribute('src');

  if (lastSrc.slice(-5).charAt(0) == ('n')) {
    weatherWidget.classList.remove("weather-day");
    weatherWidget.classList.add("weather-night");
  }

  
  function getAjax(url, success) {
    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP');
    xhr.open('GET', url);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function () {
      if (xhr.readyState > 3 && xhr.status == 200) success(xhr.responseText);
    };
    xhr.send();
    return xhr;
  }

  function getWeather() {
    getAjax("/home", function (data) {
      let json = JSON.parse(data);
      cityName.innerHTML = json.city;
      temperature.innerHTML = json.temperature + '&#176;';
      let newSrc = "../static/weathericons/" + json.icon + ".svg";
      if (lastSrc != newSrc) {
        lastSrc = newSrc;
        weatherIcon.setAttribute("src", newSrc);
      }
      if ((json.icon).slice(-1) == ('n')) {
        weatherWidget.classList.remove("weather-day");
        weatherWidget.classList.add("weather-night");
      }
      description.innerHTML = json.description;
    })
  }
  setInterval(getWeather, 60000); 