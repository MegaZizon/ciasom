
var pc=null;

function createPeerConnection() {
    var config = {
     //   sdpSemantics: 'unified-plan'
    };

    config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];

    pc = new RTCPeerConnection(config);

    // register some listeners to help debugging
    

    pc.addEventListener('iceconnectionstatechange', function() {
        if(pc.iceConnectionState=="disconnected"){alert("방송 종료됨")}
        if(pc.iceConnectionState=="connected"){
            document.getElementById('load').style.display = 'none';
        }
    }, false);

    var remoteStream = new MediaStream();
    document.getElementById('video').srcObject = remoteStream;
    pc.addEventListener('track', function(evt) {
        remoteStream.addTrack(evt.track, remoteStream);
    });

    pc.addEventListener("ended", function(event) {
        console.log("ended")
    });

    return pc;
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function negotiate() {
    try {
        console.log("gdgddasfsda")
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        await delay(3000);

        const response = await fetch('/onair/start', {
            body: JSON.stringify({
                sdp: pc.localDescription.sdp,
                type: pc.localDescription.type,
                streamid: document.getElementById('streamid').value,
                title: document.getElementById('title').value,
                category: document.getElementById('category').value,
                model: document.getElementById('video-model').value,
            }),
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });

        const answer = await response.json();
        await pc.setRemoteDescription(answer);
    } catch (e) {
        alert(e);
    }
}

function start() {
   

    document.getElementById('start').style.display = 'none';
    document.getElementById('streamerform').style.display = 'none';
    document.getElementById('media-box').style.display = 'block';
    document.getElementById('load').style.display = 'block';
    document.getElementById('stop').style.display = 'block';

    pc = createPeerConnection();

    var frame=document.getElementById('frame').value;
    
    var constraints = {
        audio: true,
        video: {
            frameRate: { ideal: frame, max: frame }, // Set your desired frame rate here (e.g., 20fps)
            // width: { ideal: 640 }, // Set your desired width here
            // height: { ideal: 480 }, // Set your desired height here
          },
    };


    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        stream.getTracks().forEach(function(track) {
            pc.addTrack(track, stream);
        });
        return negotiate();
    }, function(err) {
        alert('카메라를 불러올 수 없습니다.: ' + err);
    });

}

function stop() {
    document.getElementById('load').style.display = 'none';
    document.getElementById('media-box').style.backgroundColor = 'black';
    var stramid=document.getElementById('streamid').value;
    var href_link="/onair/end/"+stramid;
    console.log(href_link)
    $.ajax({
        url:href_link,                  
        success:function(res){
        }
    });  

    if (pc.getTransceivers) {
        pc.getTransceivers().forEach(function(transceiver) {
            if (transceiver.stop) {
                transceiver.stop();
            }
        });
    }

    pc.getSenders().forEach(function(sender) {
        sender.track.stop();
    });

    setTimeout(function() {
        pc.close();
    }, 500);
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
