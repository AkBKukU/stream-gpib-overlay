


// Poll Handling
function poll_read(poll_data)
{
    if(poll_data.length ==0)
    {
      return
    }


    devices_box = document.getElementById("devices-box");
    devices_box.textContent = '';

    for (devices of Object.entries(poll_data.devices[0]))
    {
      for (const [key, device] of Object.entries(devices))
      {
        device_new = document.createElement("div");
        device_new.classList.add("poll-box");
        title = document.createElement("h3");
        title.textContent = key;
        devices_box.appendChild(title)
        list = document.createElement("ul");
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
        devices_box.appendChild(list)
      }

      devices_box.appendChild(device_new)
    }

    poll_box = document.getElementById("poll-box");
    poll_box.classList.add('fade-in');
    poll_box.classList.remove('fade-out');
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
document.getElementById("poll-box").classList.add('fade-out');
