/* eslint-disable */

var boot = {
    didPreload: false,
    preload: async function() {
        if (this.didPreload) return;
        this.didPreload = true;
        await start.init();
        await decorations.init();
        await maker.init();
        await start.create_scene();
        await cc.set_default();
        await decorations.add_particle_system();
    },
    init: async function() {
        window.checkpoints = [];
        window.checkpointNum = 0;
        checkpoint = scene.getMeshesByTags("checkpoint")
        for(var i of checkpoint) {
            i.dispose();
        }
        await fov.init();
        await flyjump.init();
        const mapScript = document.querySelector('#map-script').innerHTML;
        eval(mapScript);
        await map.init();
        await cc.refresh()
        decorations.addOrRemoveSkybox()
        await change_state.spawn();
        // await premium.updatePremiumRequirementMet();
        await map.post();
        window.ogdistance = Math.sqrt((Math.abs(map.spawn[0]-window.end.position.x)^2)+(Math.abs(map.spawn[2]-window.end.position.z)^2))-2;
        window.ispreview = false;
        if (document.getElementById("preview").checked == true) {
            window.end.position.y = window.end.position.y+2;
            // let item = new BABYLON.Mesh.CreateBox("Endthing", .5, scene);
            // item.position = window.end.position;
            window.ispreview = true;
            document.getElementById("freeze").checked = true;
            document.getElementById("freecam").checked = true;

            // axis prioritization based on if the end goal is in the positive or negative z
            // let mainAxis = "z";
            // if (window.end.position.z > 0) {
            //     mainAxis = "x";
            // }


            sleep(10)
            // camera.position.y = map.spawn[1]+(window.ogdistance/1.55);
            // if (mainAxis == "X") {
            //     camera.position.x = map.spawn[0]-100;
            //     camera.position.z = map.spawn[2];
            // }
            // else {
            //     camera.position.x = map.spawn[0];
            //     camera.position.z = map.spawn[2]+100;
            // }
            camera.setTarget(window.end.position);
            // camera.position.x = map.spawn[0]-window.end.position.x/.8;
            // camera.position.z = map.spawn[2]-window.end.position.z/.8;
            // console.log("this map's main axis is " + mainAxis);


            // oppiset mesh solution, itteratte through all meshes under the tag mesh and find the thourthest one away from window.end.position
            let farthest = 0;
            let farthestMesh = null;
            let meshes = scene.getMeshesByTags("mesh");
            for (let mesh of meshes) {
                if (Distance3D(window.end.position.x, window.end.position.y, window.end.position.z, mesh.position.x, mesh.position.y, mesh.position.z) > farthest) {
                    farthest = Distance3D(window.end.position.x, window.end.position.y, window.end.position.z, mesh.position.x, mesh.position.y, mesh.position.z);
                    farthestMesh = mesh;
                }
            }
            camera.setTarget(farthestMesh.position);
            camera.position.x = farthestMesh.position.x - window.end.position.x/1.3;
            camera.position.z = farthestMesh.position.z - window.end.position.z/1.3;
            camera.position.y = window.end.position.y + 15;
        }
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
