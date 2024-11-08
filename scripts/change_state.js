/* eslint-disable */

var change_state = {
	die: function(deathMessage) {
		if (!alive) return
		alive = false;
		window.tsTriggers.onDeath(deathMessage);
	},
	spawn: function() {
        window.ps.dispose();
        decorations.add_particle_system();
		alive = true;
        if (window.checkpoints.length == 0) {
            score = 0;
        }
		flyjump.last_frame = 0;
        rotation = 0
		// rotation = document.getElementById("PracticeR").value;
		spectateAnimationValue = 5;
		// world
		player.rotationQuaternion = BABYLON.Quaternion.RotationAxis(new BABYLON.Vector3(0,0,0),0);
		player.physicsImpostor.setLinearVelocity(new BABYLON.Vector3(0,0,0));
		player.physicsImpostor.setAngularVelocity(new BABYLON.Quaternion(0,1,0,0));
        if (window.checkpoints.length <= 0) {
		    player.position = new BABYLON.Vector3(map.spawn[0],map.spawn[1],map.spawn[2]);
            player.rotation = new BABYLON.Vector3(0,0,0);
        }
        else {
            player.position = new BABYLON.Vector3(window.checkpoints.at(-1)[0],window.checkpoints.at(-1)[1],window.checkpoints.at(-1)[2]);
            player.rotation = new BABYLON.Vector3(0,0,0);
            rotation = parseFloat(window.checkpoints.at(-1)[3]);
        }
		cc.refresh();
		map.reset();
        if (document.getElementById("spawnX").value != "") {player.position.x = parseFloat(document.getElementById("spawnX").value);}
        if (document.getElementById("spawnY").value != "") {player.position.y = parseFloat(document.getElementById("spawnY").value);}
        if (document.getElementById("spawnZ").value != "") {player.position.z = parseFloat(document.getElementById("spawnZ").value);}
        // if (document.getElementById("spawnR").value != "") {let angleDegrees = parseFloat(document.getElementById("spawnR").value);let angleRadians = angleDegrees * (Math.PI / 180);rotation = angleRadians / 60;}
        if (document.getElementById("spawnR").value != "") {rotation = parseFloat(document.getElementById("spawnR").value);}

        if (document.getElementById("follow").checked == true) {
            camera.position = new BABYLON.Vector3(map.spawn[0],player.position.y+window.followHeight,player.position.z+window.followDistance);
        }

	}, 
	win: function() {
		if (!alive) return
		alive = false;
		window.tsTriggers.onWin()
	}
}