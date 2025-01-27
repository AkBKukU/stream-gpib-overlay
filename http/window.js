


// Poll Handling
function poll_read(poll_data)
{
    devices_box = document.getElementById("devices-box");
    if(poll_data.length ==0)
    {
        devices_box.classList.add('fade-out');
        devices_box.classList.remove('fade-in');
      return
    }

    devices_box.classList.add('fade-in');
    devices_box.classList.remove('fade-out');


    devices_box.textContent = '';

    for (devices of poll_data.devices)
    {
      for (const [key, device] of Object.entries(devices))
      {
        device_new = document.createElement("div");
        device_new.classList.add("poll-box");
        title = document.createElement("h3");
        title.classList.add("poll-title");
        title.textContent = key;
        device_new.appendChild(title)
        list = document.createElement("ul");
        list.classList.add("poll-list");
        for (const [reading, value] of Object.entries(device))
        {
          li = document.createElement("li");

          var text = document.createElement("span");
          text.innerHTML = reading
          text.classList.add("poll-text");
          li.appendChild(text)

          var count = document.createElement("span");
          count.innerHTML = value
          count.classList.add("poll-count");
          li.appendChild(count)
          list.appendChild(li)
        }
        device_new.appendChild(list)
      }

      devices_box.appendChild(device_new)
    }
}


// Poll Data Loop
function poll_fetch()
{
  fetch('/dev/gpib_data.json')
    .then((response) => response.json())
    .then((data) => poll_read(data));

  setTimeout(poll_fetch,1000)
}



// Final Init
setTimeout(poll_fetch,1000)
document.getElementById("devices-box").classList.add('fade-out');
