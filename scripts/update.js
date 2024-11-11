/* eslint-disable */
var update = {
	loop: function() {
		if (!isMapLoaded || window.paused) return
		scene.render();
		if (isSpectating) {
			this.loopWhileSpectating();
		} else if (alive) {
			this.loopWhilePlaying();
		}
	},
	loopWhileSpectating() {
		spectateAnimationValue += 1;

		camera.rotation.x = 0.1 + Math.sqrt(spectateAnimationValue * 0.0015);
		camera.rotation.z = 0;
		camera.rotation.y = Math.PI;

		camera.position.x = 0;
		camera.position.z = -0.2 * spectateAnimationValue;
		camera.position.y = 2 + 0.2 * spectateAnimationValue;
	},
	loopWhilePlaying() {
        if (!window.ispreview) {
            try {
                score += 1;
                window.tsTriggers.onFrame()
                // render call
                this.player_move();
                map.render_update();
                map.section_update();
                flyjump.render_loop();
                // physics call
                if (score % physics_call_rate == 0) {
                    // god mode
                    this.collision_check();
                    map.physics_update();
                    flyjump.compute_loop();
                    this.update_overlay();
                }
                if (document.getElementById("fog").checked) {
                    scene.getMeshByName("fog").position = player.position;
                    scene.getMeshByName("fog2").position = player.position;
                }
            } catch(err) {
                console.log(err);
            }
        }
        else {
            this.preview();
        }
	},
    // spesific god mode
	collision_check: function() {
        let godmodeCheckbox = document.getElementById("godmode");
        let freeze = document.getElementById("freeze");
        if (!godmodeCheckbox.checked) {
            if (player.position.y < -20) {change_state.die('Fell To Death')}
            if (player.position.y > 80) {change_state.die('Left The Orbit')}
            this.checkConeCollision()
        }
        this.checkEndingCollision()
	},
	checkConeCollision() {
		for (let i=0;i<maker.cone_count;i++) {
			let cone = cones[i];
			if (this.are_touching(player, cone, 0.5)) {
				change_state.die('Died From Cone');
				break;
			}
		}
	},
	checkEndingCollision() {
		if (score < 10) return
		for (let i=0;i<maker.ending_count;i++) {
			let ending = endings[i];
			if (this.are_touching(player, ending, 1.2)) { // previously 1.0
				change_state.win();
				break;
			}
		}
	},
	player_move: function() {
		// steer
		if ((controls.space) && (score > 10)) {
			flyjump.jump();
		}
		if (!this.shouldSpin()) {
			player.physicsImpostor.setAngularVelocity(new BABYLON.Vector3(0,0,0));
			player.rotationQuaternion = BABYLON.Quaternion.RotationAxis(new BABYLON.Vector3(0,0,0),0);
		}
		const rotationAdjustment = window.tsTriggers.getRotationAdjustment()
		rotation += rotationAdjustment
		player.rotation.y = rotation;

        let freeze = document.getElementById("freeze");
        if (window.platformermode) {}
        else if (freeze.checked == false) {
            const positionAdjustment = window.tsTriggers.getPositionAdjustment()
            player.position.x += positionAdjustment.x;
            player.position.z += positionAdjustment.z;
        }
		// light & camera
        let freecam = document.getElementById("freecam");
        let follow = document.getElementById("follow"); // these 2 are just the checkboxes, you can change the toggle
        let fpv = document.getElementById("fpv");
        if (fpv.checked) {
            camera.position.x = player.position.x;
            camera.position.z = player.position.z;
            camera.position.y = player.position.y + 0.25;

            camera.rotation = player.rotation;
            camera.rotation.x += Math.PI;
            camera.position.y += 0.25;
        }
        else if (!freecam.checked) { // your code, normal camera movement if it's turned off, so if it's triggered it "unhooks" the camera from the player
            let rotation_offsetted = rotation + cameraRightAngle;
            camera.position.x = player.position.x + Math.sin(rotation_offsetted) * cam_horizontal;
            camera.position.z = player.position.z + Math.cos(rotation_offsetted) * cam_horizontal;
            camera.position.y = player.position.y + cam_vertical;
            camera.rotation.y = 3.14 + rotation_offsetted;
            camera.rotation.x = cam_depression;
        }
        else if (follow.checked) { // follow player script, only works if the camera is "unhooked"
            const lerp = (start, end, t) => start * (1 - t) + end * t;
            const targetY = player.position.y + window.followHeight;
            const baseSmoothingFactor = 0.05; // a smoothing function to practically remove jitter

            camera.setTarget(player.position); // look at player

            const distanceX = Math.abs(player.position.x - camera.position.x);
            const distanceZ = Math.abs(player.position.z - camera.position.z);

            // Adjust smoothing factor based on distance
            const smoothingFactorX = baseSmoothingFactor * Math.min(distanceX / window.followDistance, 1);
            const smoothingFactorZ = baseSmoothingFactor * Math.min(distanceZ / window.followDistance, 1);

            // apply smoothing
            camera.position.x = lerp(camera.position.x, player.position.x, smoothingFactorX);
            camera.position.z = lerp(camera.position.z, player.position.z, smoothingFactorZ);
            camera.position.y = lerp(camera.position.y, targetY, baseSmoothingFactor);
        }
		light.position = camera.position;
	},
	shouldSpin: function() {
        let spinCheckbox = document.getElementById("spin");
        if (spinCheckbox.checked == false) {
            if (flyjump.can_jump) return false;
            if (speed === default_speed) return true;
            if (speed === 0.2) return true;
            return false
        }
        else {return false;}
	},
	are_touching: function(a, b, r) {
		let dz = a.position.z - b.position.z;
		if (Math.abs(dz) < r) {
			let dx = a.position.x - b.position.x;
			if (Math.abs(dx) < r) {
				let dy = a.position.y - b.position.y;
				if (Math.abs(dy) < r * 1.5) {
					return true;
				}
			}
		}
		return false;
	},
	set_gravity: function(val) {
        let gravitytoggle = document.getElementById("gravityoverwrite")
		if (!gravitytoggle.checked) {
            scene.gravity = new BABYLON.Vector3(0, val, 0);
            gravity = scene.gravity;
            scene.getPhysicsEngine().setGravity(scene.gravity);
            player.applyGravity = true;
        }
	},
	update_overlay: function() {
		const isJumpEnabled = flyjump.can_jump;
		cape_wings.isVisible = isJumpEnabled;
		window.tsTriggers.setJumpEnabledSignVisibility(isJumpEnabled);

        window.tsTriggers.setPlatformerSignVisibility(window.platformermode);

		const isControlsReversed = (steer < 0);
		cape_tail.isVisible = isControlsReversed;
		window.tsTriggers.setControlsReversedSignVisibility(isControlsReversed);

		window.tsTriggers.setDriftEnabledSignVisibility(isTouchingDriftPad);
	},
    preview: function() {
        const lerp = (start, end, t) => start * (1 - t) + end * t;
        // slowly step camera towards window.end.position
        let yOffset = 0;
        if (camera.position.y < window.end.position.y) {yOffset = Math.abs(end.position.y - camera.position.y)/50}
        else {yOffset = 0}
        camera.setTarget(window.end.position);
        camera.position.x = lerp(camera.position.x, window.end.position.x, 0.004);
        camera.position.z = lerp(camera.position.z, window.end.position.z, 0.004);
        // camera.position.y = lerp(camera.position.y + yOffset, window.end.position.y + 2, 0.00075);

        // ray solution (doesn't work on short maps
        if (Distance3D(camera.position.x, camera.position.y, camera.position.z, window.end.position.x, window.end.position.y, window.end.position.z) < 20) {
            window.ispreview = false;
            document.getElementById("freeze").checked = false;
            document.getElementById("freecam").checked = false;
            alert("Preview mode ended");
            // for (let i=0;i<window.objectsHit.length;i++) {
            //     window.objectsHit[i].material.alpha = window.ogAlphaHit[i];
            //     console.log("undid hit for " + window.objectsHit[i].name + " with alpha " + window.ogAlphaHit[i]);
            // }
        }
        // // anti-hit logic
        // let direction = window.end.position.subtract(camera.position).normalize();

        // let ray = new BABYLON.Ray(camera.position, direction);
        // let hit = scene.pickWithRay(ray, (mesh) => {
        //     // filter out the ends and cones
        //     return mesh.name.substring(0,1) != "E" && mesh.name.substring(0,1) != "C";
        // });
        // window.objectsHit = [];
        // window.ogAlphaHit = [];
        // let hitDistance = null;
        // let hitPoint = null;
        // if (hit.pickedMesh) {
        //     hitDistance = hit.distance;
        //     hitPoint = hit.pickedPoint;
        //     if (hitDistance <= 80) {
        //         console.log("no good, Hit ", hit.pickedMesh.name + " at " + hit.pickedPoint + " with distance " + hit.distance);
        //         try{hit.pickedMesh.material.alpha = 0.35;
        //         window.objectsHit.push(hit.pickedMesh);
        //         window.ogAlphaHit.push(hit.pickedMesh.material.alpha);
        //         } catch(err) {}
        //     }
        // } else {
        //     console.log("good");
        //     hitDistance = null;
        //     hitPoint = null;
        // }
    }
}
function Distance3D(x1, y1, z1, x2, y2, z2) {
    return Math.sqrt(
        Math.abs(Math.pow(x2 - x1, 2)) +
        Math.abs(Math.pow(y2 - y1, 2)) +
        Math.abs(Math.pow(z2 - z1, 2))
    );
}