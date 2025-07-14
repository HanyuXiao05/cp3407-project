const staffHours = {
  "Monday": [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  "Tuesday": [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  "Wednesday": [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  "Thursday": [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  "Friday": [["06:00", "08:00"], ["12:00", "14:00"], ["18:00", "20:00"]],
  "Saturday": [["07:00", "13:00"]]
};

const studentHours = {
  "Monday": [["08:00", "22:00"]],
  "Tuesday": [["08:00", "22:00"]],
  "Wednesday": [["08:00", "22:00"]],
  "Thursday": [["08:00", "22:00"]],
  "Friday": [["08:00", "22:00"]],
  "Saturday": [["08:00", "18:00"]]
};

// Convert "HH:MM" to number of minutes
function timeToMinutes(t) {
  const [h, m] = t.split(":").map(Number);
  return h * 60 + m;
}

// Convert minutes back to "HH:MM"
function minutesToTime(m) {
  const h = Math.floor(m / 60).toString().padStart(2, '0');
  const min = (m % 60).toString().padStart(2, '0');
  return `${h}:${min}`;
}

function getDayOfWeek(dateString) {
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  return days[new Date(dateString).getDay()];
}

function generateSlots(ranges) {
  const slots = [];
  for (const [start, end] of ranges) {
    let s = timeToMinutes(start);
    const e = timeToMinutes(end);
    while (s + 60 <= e) {
      const from = minutesToTime(s);
      const to = minutesToTime(s + 60);
      slots.push(`${from} - ${to}`);
      s += 60;
    }
  }
  return slots;
}

function updateTimeSlots() {
  const userType = document.getElementById('userType').value;
  const date = document.getElementById('date').value;
  const timeSlotList = document.getElementById('timeSlotList');
  timeSlotList.innerHTML = "";

  if (!date) return;

  const day = getDayOfWeek(date);
  const ranges = userType === "staff" ? staffHours[day] : studentHours[day];
  if (!ranges) {
    timeSlotList.innerHTML = "<p>No available slots on this day.</p>";
    return;
  }

  const slots = generateSlots(ranges);
  slots.forEach((slot, i) => {
    const div = document.createElement("div");
    div.className = "slot-item";
    const input = document.createElement("input");
    input.type = "checkbox";
    input.id = `slot-${i}`;
    input.name = "timeSlot";
    input.value = slot;

    input.addEventListener('change', () => {
      const checked = document.querySelectorAll('input[name="timeSlot"]:checked');
      if (checked.length > 2) {
        input.checked = false;
        alert("You can only book up to 2 time slots per day.");
      }
    });

    const label = document.createElement("label");
    label.htmlFor = `slot-${i}`;
    label.textContent = slot;

    div.appendChild(input);
    div.appendChild(label);
    timeSlotList.appendChild(div);
  });
}

document.getElementById('date').addEventListener('change', updateTimeSlots);
document.getElementById('userType').addEventListener('change', updateTimeSlots);

function confirmBooking() {
  const userType = document.getElementById('userType').value;
  const date = document.getElementById('date').value;
  const selectedSlots = Array.from(document.querySelectorAll('input[name="timeSlot"]:checked'))
                             .map(cb => cb.value);

  if (!date || selectedSlots.length === 0) {
    alert("Please select a valid date and at least one time slot.");
    return;
  }

  alert(`Booking confirmed for ${userType} on ${date} at:\n${selectedSlots.join(', ')}`);
}
