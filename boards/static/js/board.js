(function () {
  var script = document.currentScript;
  var moveTemplate = script && script.dataset.moveUrl ? script.dataset.moveUrl : "/tasks/0/move/";
  var csrf = document.cookie
    .split("; ")
    .map(function (c) { return c.split("="); })
    .filter(function (p) { return p[0] === "csrftoken"; })
    .map(function (p) { return p[1]; })[0];

  function moveUrl(taskId) {
    return moveTemplate.replace("/0/move/", "/" + taskId + "/move/");
  }

  function moveTask(card, status) {
    var select = card.querySelector(".status-select");
    if (select) select.value = status;
    var current = card.closest(".column");
    fetch(moveUrl(card.dataset.taskId), {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest", "X-CSRFToken": csrf },
      body: new URLSearchParams({ status: status })
    })
      .then(function (res) {
        if (!res.ok) { window.location.reload(); return res.json(); }
        return res.json();
      })
      .then(function (data) {
        if (!data || !data.ok) { window.location.reload(); return; }
        var target = document.querySelector('.column[data-status="' + status + '"] .cards');
        if (target && current !== target.parentElement) {
          target.appendChild(card);
        } else {
          window.location.reload();
        }
        document.querySelectorAll(".column").forEach(function (col) {
          var n = col.querySelectorAll(".task-card").length;
          var badge = col.querySelector(".count");
          if (badge) badge.textContent = n;
          var empty = col.querySelector(".empty-col");
          if (empty && n > 0) empty.remove();
          if (!empty && n === 0) {
            var p = document.createElement("p");
            p.className = "muted empty-col";
            p.textContent = "Пусто";
            col.querySelector(".cards").appendChild(p);
          }
        });
      })
      .catch(function () { window.location.reload(); });
  }

  document.addEventListener("change", function (e) {
    var select = e.target.closest(".status-select");
    if (!select) return;
    var form = select.closest("form");
    var card = select.closest(".task-card");
    e.preventDefault();
    moveTask(card, select.value);
  });

  var dragged = null;

  document.addEventListener("dragstart", function (e) {
    var card = e.target.closest(".task-card.draggable");
    if (!card) { return; }
    dragged = card;
    card.classList.add("dragging");
    e.dataTransfer.setData("text/plain", card.dataset.taskId);
    e.dataTransfer.effectAllowed = "move";
  });

  document.addEventListener("dragend", function () {
    if (dragged) dragged.classList.remove("dragging");
    dragged = null;
    document.querySelectorAll(".column.drag-over").forEach(function (c) { c.classList.remove("drag-over"); });
  });

  document.querySelectorAll(".column").forEach(function (col) {
    col.addEventListener("dragover", function (e) {
      if (!dragged || !dragged.classList.contains("draggable")) return;
      e.preventDefault();
      col.classList.add("drag-over");
    });
    col.addEventListener("dragleave", function () { col.classList.remove("drag-over"); });
    col.addEventListener("drop", function (e) {
      e.preventDefault();
      col.classList.remove("drag-over");
      if (!dragged) return;
      var status = col.dataset.status;
      if (dragged.closest(".column") === col) { dragged = null; return; }
      moveTask(dragged, status);
      dragged = null;
    });
  });
})();
