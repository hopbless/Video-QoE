
		var tag = document.createElement('script');

		tag.src = "https://www.youtube.com/iframe_api";
		var firstScriptTag = document.getElementsByTagName('script')[0];
		firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
		
		var player;
		function onYouTubeIframeAPIReady() {
		player = new YT.Player('player', {
			height: '390',
			width: '640',
			videoId: 'M7lc1UVf-VE',
			playerVars: {
			'playsinline': 1
			},
			events: {
			'onReady': onPlayerReady,
			'onStateChange': onPlayerStateChange
			}

		})

		

		
		};

		// The API will call this function when the video player is ready.
		function onPlayerReady(event) {
		event.target.playVideo();
		run();
		};

		// 5. The API calls this function when the player's state changes.
		//    The function indicates that when playing a video (state=1),
		//    the player should play for six seconds and then stop.
		var done = false;
		function onPlayerStateChange(event) {
		if (event.data == YT.PlayerState.PLAYING && !done) {
			setTimeout(stopVideo, 6000)
			done = true;
		};
		};

		function stopVideo() {
		player.stopVideo();
		};

		function run(){
			getInfos();

		if (x <= 3600){

			var currentTime = player.getCurrentTime;
			//var i = player.buffered.length;
			var availablePlaybackTime = player.getDuration;
			var bufferedTime = availablePlaybackTime - currentTime;
			var percentBufferedVideo = getVideoLoadedFraction * 100
			outC = outC + new Date().getTime() + "#" +  currentTime + "#" + bufferedTime + "#" + availablePlaybackTime + "#" + percentBufferedVideo + "\n";
			document.getElementById("outC").innerHTML = outC;
			document.getElementById("outE").innerHTML = outE;
			//console.log("Video outE", outE)
			x++;
			setTimeout(run, 1000);
		}else {
		}

		};

		function getInfos(){
			var currentTime = new Date().getTime();
		
			var videoHeight = player.videoHeight;
			if(last_videoHeight != videoHeight){
				last_videoHeight = videoHeight;
				var videoWidth = player.videoWidth;
				var infos = "quality:"+ videoHeight + "p" + " (" + videoWidth + "x" + videoHeight + ")";
				outE = outE + currentTime + "#" + infos + "\n";
				
			}
		
			var volume = player.volume;
			if(last_volume != volume){
				last_volume = volume;
				var infos = "volume:"+ volume + "";
				outE = outE + currentTime + "#" + infos + "\n";
			}
		
			var duration = player.duration;
			if(last_duration != duration){
				last_duration = duration;
				var infos = "duration:"+ duration + "";
				outE = outE + currentTime + "#" + infos + "\n";
			}
		
			var ytid = getYouTubeID();
			if(last_ytid != ytid){
				last_ytid = ytid;
				var infos = "ytid:"+ ytid + "";
				outE = outE + currentTime + "#" + infos + "\n";
			}
		
			var title = getTitle();
			if(last_title != title){
				last_title = title;
				var infos = "title:"+ title + "";
				outE = outE + currentTime + "#" + infos + "\n";
			}        
		};
