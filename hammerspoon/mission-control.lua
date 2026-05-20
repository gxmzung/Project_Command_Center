local html = [[
<html>
<body style="
  margin:0;
  padding:22px;
  background:rgba(20,20,25,0.92);
  color:white;
  font-family:-apple-system, BlinkMacSystemFont, sans-serif;
">
  <h1 style="color:#7dd3fc;font-size:26px;margin:0 0 18px 0;">MISSION CONTROL</h1>

  <h3 style="color:#22c55e;margin-bottom:8px;">HIGH PRIORITY</h3>
  <p style="line-height:1.7;margin-top:0;">
    CityBrain<br>
    SkyEdge / ROS2 PX4<br>
    UAM Radio Environment
  </p>

  <h3 style="color:#facc15;margin-bottom:8px;">ACTIVE COMPETITIONS</h3>
  <p style="line-height:1.7;margin-top:0;">
    ADD Defense<br>
    K-Mobility<br>
    Sejong Idea Competition
  </p>

  <h3 style="color:#a78bfa;margin-bottom:8px;">RESEARCH / EXPANSION</h3>
  <p style="line-height:1.7;margin-top:0;">
    BioDockLab<br>
    Campus OS / 배재Pick
  </p>

  <p style="color:#aaa;border-top:1px solid #555;padding-top:12px;">
    Build real systems.
  </p>
</body>
</html>
]]

dashboard = hs.webview.new({x=1100, y=80, w=390, h=520})
dashboard:html(html)
dashboard:windowStyle({"utility", "HUD", "titled", "closable"})
dashboard:level(hs.drawing.windowLevels.floating)
dashboard:show()

hs.alert.show("MISSION CONTROL LOADED")
