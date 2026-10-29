(function () {
  // Shop hours in Oxnard (Pacific time). Keep in sync with the hours list and the LocalBusiness JSON-LD.
  // Index is the day of the week, Sunday = 0. Each entry is [opens, closes] in 24-hour time, or null.
  const hours = [null, [10, 18], [10, 18], [10, 18], [10, 18], [10, 18], [12, 15]];
  const spanish = (document.documentElement.lang || "").toLowerCase().startsWith("es");

  const words = spanish
    ? {
        days: ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"],
        time: (h) =>
          h === 12 ? "las 12 del mediodía" : h < 12 ? `las ${h} de la mañana` : `las ${h - 12} de la tarde`,
        openNow: (close) => `Estamos abiertos ahora, hasta ${close}.`,
        laterToday: (open) => `Hoy abrimos a ${open}. Puede llamar ahora y dejar un mensaje, o escribirnos.`,
        closed: (when) => `Ahora estamos cerrados. Abrimos ${when}. Deje un mensaje y le devolvemos la llamada.`,
        when: (ahead, day, open) => (ahead === 1 ? `mañana a ${open}` : `el ${day} a ${open}`),
        today: (open) => `hoy a ${open}`,
        reply: {
          open: "Estamos abiertos ahora, así que es posible que le llamemos hoy mismo.",
          closed: (when) => `Ahora estamos cerrados. Le llamaremos cuando abramos, ${when}.`,
        },
      }
    : {
        days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        time: (h) => (h === 12 ? "12\u00a0PM" : h < 12 ? `${h}\u00a0AM` : `${h - 12}\u00a0PM`),
        openNow: (close) => `We're open now, until ${close}.`,
        laterToday: (open) => `We open today at ${open}. You can call now and leave a message, or write to us.`,
        closed: (when) =>
          `We're closed now and open again ${when}. Leave a message, and we'll call you back.`,
        when: (ahead, day, open) => `${ahead === 1 ? "tomorrow" : day} at ${open}`,
        today: (open) => `today at ${open}`,
        reply: {
          open: "We're open now, so you may hear from us today.",
          closed: (when) => `We're closed right now. We'll reach out when we open, ${when}.`,
        },
      };

  const nowInOxnard = () => {
    const parts = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/Los_Angeles",
      weekday: "short",
      hour: "numeric",
      minute: "numeric",
      hourCycle: "h23",
    }).formatToParts(new Date());
    const get = (type) => parts.find((part) => part.type === type)?.value;
    const day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(get("weekday"));
    return { day, time: Number(get("hour")) + Number(get("minute")) / 60 };
  };

  const status = () => {
    const { day, time } = nowInOxnard();
    const today = hours[day];
    if (today && time >= today[0] && time < today[1]) {
      return { open: true, text: words.openNow(words.time(today[1])), reply: words.reply.open };
    }
    if (today && time < today[0]) {
      const open = words.time(today[0]);
      return { open: false, text: words.laterToday(open), reply: words.reply.closed(words.today(open)) };
    }
    for (let ahead = 1; ahead <= 7; ahead += 1) {
      const next = (day + ahead) % 7;
      if (!hours[next]) continue;
      const when = words.when(ahead, words.days[next], words.time(hours[next][0]));
      return { open: false, text: words.closed(when), reply: words.reply.closed(when) };
    }
    return null;
  };

  const current = status();
  if (!current) return;

  document.querySelectorAll("[data-open-status]").forEach((element) => {
    element.textContent = element.hasAttribute("data-open-status-reply") ? current.reply : current.text;
    element.classList.toggle("is-open", current.open);
    element.hidden = false;
  });

  const todayRow = document.querySelector(`.hours [data-days~="${nowInOxnard().day}"]`);
  todayRow?.classList.add("is-today");
})();
