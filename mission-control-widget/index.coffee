command: "echo MissionControl"

refreshFrequency: 5000

style: """
  top: 30px
  right: 30px
  width: 360px
  background: rgba(15,15,15,0.88)
  color: #f5f5f5
  padding: 22px
  border-radius: 18px
  font-family: SF Pro Display
  box-shadow: 0 0 25px rgba(0,0,0,0.45)
  backdrop-filter: blur(12px)
  z-index: 9999
"""

render: -> """
<div class="wrapper">

<div class="title">
MISSION CONTROL
</div>

<div class="section">
<div class="sectionTitle">HIGH PRIORITY</div>
<ul>
<li>CityBrain</li>
<li>SkyEdge</li>
<li>UAM Radio Environment</li>
</ul>
</div>

<div class="section">
<div class="sectionTitle">MEDIUM PRIORITY</div>
<ul>
<li>ADD Defense</li>
<li>BioDockLab</li>
<li>K-Mobility</li>
<li>Sejong Competition</li>
</ul>
</div>

<div class="section">
<div class="sectionTitle">THIS WEEK</div>
<ul>
<li>ROS2 PX4</li>
<li>CS Fundamentals</li>
<li>GitHub Cleanup</li>
<li>Competition Docs</li>
</ul>
</div>

<div class="section">
<div class="sectionTitle">LONG TERM</div>
<div class="goal">
Mission Software Engineer
</div>
<div class="goal">
Systems Architect
</div>
<div class="goal">
Technical PM
</div>
</div>

<div class="quote">
"Build real systems."
</div>

</div>
"""

afterRender: (domEl) ->
  title = domEl.querySelector(".title")
  title.style.fontSize = "28px"
  title.style.fontWeight = "700"
  title.style.marginBottom = "20px"
  title.style.color = "#00d9ff"

  sections = domEl.querySelectorAll(".section")
  for section in sections
    section.style.marginBottom = "18px"

  sectionTitles = domEl.querySelectorAll(".sectionTitle")
  for st in sectionTitles
    st.style.fontSize = "15px"
    st.style.fontWeight = "700"
    st.style.marginBottom = "8px"
    st.style.color = "#00ff99"

  lists = domEl.querySelectorAll("ul")
  for list in lists
    list.style.paddingLeft = "18px"

  items = domEl.querySelectorAll("li")
  for item in items
    item.style.marginBottom = "6px"

  goals = domEl.querySelectorAll(".goal")
  for goal in goals
    goal.style.marginBottom = "5px"

  quote = domEl.querySelector(".quote")
  quote.style.marginTop = "20px"
  quote.style.fontStyle = "italic"
  quote.style.color = "#888"