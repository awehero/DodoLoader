var map = {
    title: "EngineV9",
    song: "env2",
    maker: "Gui",
    spawn: [0, 0.5, 0],
    init: function() {
        document.getElementById("freeze").checked = true;
        document.getElementById("spin").checked = true;
        document.getElementById("freecam").checked = true;
        document.getElementById("ObjectSelector").innerHTML = "<option> </option>";
        camera.position = new BABYLON.Vector3(0,5,+5);
        camera.rotation.x = 19.5

        // const box = BABYLON.MeshBuilder.CreateBox("box", options={size:2}, scene);
        // box.renderOutline = true
        // box.outlineColor = new BABYLON.Color3(0, 1, 0);
        // box.outlineWidth = 0.1;
        // point 1 | rotation | point 2
        a.p([0, -1.0, 0], [0, 0, 0], [2.5, 1.0, 2.5], 0, 0);
    },
    post: function() {},
    section_id: 0,
    section_update: function() {},
    reset: function() {
        a.re('P0', [0, -1.0, 0], [0, 0, 0], [2.5, 1.0, 2.5]);
    },
    player_move: function() {},
    physics_update: function() {},
    render_update: function() {},
}