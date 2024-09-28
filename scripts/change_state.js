/* eslint-disable */

var change_state = {
	die: function(deathMessage) {
		if (!alive) return
		alive = false;
		window.tsTriggers.onDeath(deathMessage);
	},
	spawn: function() {
		alive = true;
		score = 0;
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
	}, 
	win: function() {
		if (!alive) return
		alive = false;
		window.tsTriggers.onWin()
	}
}