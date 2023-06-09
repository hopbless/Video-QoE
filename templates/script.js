
		
		var player;
		
		function onYouTubeIframeAPIReady() {
			//'use strict';
		
			var inputVideoId = document.getElementById('YouTube-video-id');
			var videoId = inputVideoId.value;
			var suggestedQuality = 'hd720';
			var height = 390;
			var width = 640;
			var youTubePlayerVolumeItemId = 'YouTube-player-volume';
		
		
			function onError(event) {
				player.personalPlayer.errors.push(event.data);
			}
		
		
			function onPlayerReady(event) {
				var YTplayer = event.target;
		
				YTplayer.loadVideoById({suggestedQuality: suggestedQuality,
									  videoId: videoId
									 });
				
				YTplayer.playVideo();
				run();
				youTubePlayerDisplayFixedInfos();
			}
		
		
			function onPlayerStateChange(event) {
				var volume = Math.round(event.target.getVolume());
				var volumeItem = document.getElementById(youTubePlayerVolumeItemId);
		
				if (volumeItem && (Math.round(volumeItem.value) != volume)) {
					volumeItem.value = volume;
				}

				if (event.data == YT.PlayerState.PLAYING) {
					var currentTime = new Date().getTime();
					var infos = event;
					let infoData = event.data
					outE = outE + currentTime + "#" + infos + "#" + infoData + "\n";
		
				}else if (event.data == YT.PlayerState.ENDED){
					var currentTime = new Date().getTime();
					var infos = event;
					let infoData = event.data
					outE = outE + currentTime + "#" + infos + "#" + infoData + "\n";
		
				}else if (event.data == YT.PlayerState.PAUSED){
					var currentTime = new Date().getTime();
					var infos = event;
					let infoData = event.data
					outE = outE + currentTime + "#" + infos + "#" + infoData + "\n";
		
				}else if (event.data == YT.PlayerState.BUFFERING){
					var currentTime = new Date().getTime();
					var infos = event;
					let infoData = event.data
					outE = outE + currentTime + "#" + infos + "#" + infoData + "\n";
		
				}else if (event.data == YT.PlayerState.CUED){
					var currentTime = new Date().getTime();
					var infos = event;
					let infoData = event.data
					outE = outE + currentTime + "#" + infos + "#" + infoData + "\n";
				
				};
			}

			function onPlayerPlaybackQualityChange(event){
				var currentTime = new Date().getTime();
				var infos = event;
				let infoData = event.data
				outE = outE + currentTime + "#" + infos + "#" + infoData + "\n";

			}
		
		
			player = new YT.Player('YouTube-player',
										  {videoId: videoId,
										   height: height,
										   width: width,
										   playerVars: {'autohide': 0,
														'cc_load_policy': 0,
														'controls': 2,
														'disablekb': 1,
														'autoplay' : 1,
														'iv_load_policy': 3,
														'modestbranding': 1,
														'rel': 0,
														'showinfo': 0,
														'enablejsapi' : 1
													   },
										   events: {'onError': onError,
													'onReady': onPlayerReady,
													'onStateChange': onPlayerStateChange,
													'onPlaybackQualityChange': onPlayerPlaybackQualityChange
												   }
										  });
		
			// Add private data to the YouTube object
			player.personalPlayer = {'currentTimeSliding': false,
											'errors': []};
		}
		
		
		
		function playerActive() {
			'use strict';
		
			return player && player.hasOwnProperty('getPlayerState');
		}
		

		function run(){
			getInfos();

		if (x <= 3600){

			var currentPlayTime = player.getCurrentTime();
			//var i = player.buffered.length;
			var availablePlaybackTime = player.getDuration();
			var bufferedTime = availablePlaybackTime - currentPlayTime;
			var percentBufferedVideo = (player.getVideoLoadedFraction() * 100).toFixed(1)
			outC = outC + new Date().getTime() + "#" +  currentPlayTime + "#" + bufferedTime + "#" + availablePlaybackTime + "#" + percentBufferedVideo + "\n";
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
		
			var infos = "quality:"+ suggestedQuality ;
			outE = outE + currentTime + "#" + infos + "\n";

			var infos = videoId.value;
			outE = outE + currentTime + "#" + infos + "\n";

			
			var infos = player.getDuration;
			outE = outE + currentTime + "#" + infos + "\n";
  
	
		};
		
		function youTubePlayerChangeVideoId() {
			//'use strict';
		
			var inputVideoId = document.getElementById('YouTube-video-id');
			var videoId = inputVideoId.value;
		
			player.loadVideoById({'videoId': videoId});
			player.playVideo();

			run()
			youTubePlayerDisplayFixedInfos();
		}

		function youTubePlayerDisplayFixedInfos() {
			'use strict';
		
			if (playerActive()) {
				document.getElementById('YouTube-player-fixed-infos').innerHTML = (
					'Embed code: <textarea readonly>' + player.getVideoEmbedCode() + '</textarea>'
				);
			}
		}

		function youTubePlayerDisplayInfos() {
			//'use strict';
		
			if ((this.nbCalls === undefined) || (this.nbCalls >= 3)) {
				this.nbCalls = 0;
			}
			else {
				++this.nbCalls;
			}
		
			var indicatorDisplay = '<span id="indicator-display" title="timing of informations refreshing">' + ['|', '/', String.fromCharCode(8212), '\\'][this.nbCalls] + '</span>';
		
			if (playerActive()) {
				var state = player.getPlayerState();
		
				var current = player.getCurrentTime();
				var duration = player.getDuration();
				var currentPercent = (current && duration
									  ? current*100/duration
									  : 0);
		
				var fraction = (player.hasOwnProperty('getVideoLoadedFraction')
								? player.getVideoLoadedFraction()
								: 0);
		
				var url = player.getVideoUrl();
		
				if (!current) {
					current = 0;
				}
				if (!duration) {
					duration = 0;
				}
		
				var volume = player.getVolume();
		
				if (!player.personalPlayer.currentTimeSliding) {
					document.getElementById('YouTube-player-progress').value = currentPercent;
				}
		
				document.getElementById('YouTube-player-infos').innerHTML = (
					indicatorDisplay
						+ 'URL: <a class="url" href="' + url + '">' + url + '</a><br>'
						+ 'Quality: <strong>' + player.getPlaybackQuality() + '</strong>'
						+ ' &mdash; Available quality: <strong>' + player.getAvailableQualityLevels() + '</strong><br>'
						+ 'State <strong>' + state + '</strong>: <strong>' + youTubePlayerStateValueToDescription(state) + '</strong><br>'
						+ 'Loaded: <strong>' + (fraction*100).toFixed(1) + '</strong>%<br>'
						+ 'Duration: <strong>' + current.toFixed(2) + '</strong>/<strong>' + duration.toFixed(2) + '</strong>s = <strong>' + currentPercent.toFixed(2) + '</strong>%<br>'
						+ 'Volume: <strong>' + volume + '</strong>%'
				);
		
				document.getElementById('YouTube-player-errors').innerHTML = '<div>Errors: <strong>' + player.personalPlayer.errors + '</strong></div>';
			}
			else {
				document.getElementById('YouTube-player-infos').innerHTML = indicatorDisplay;
			}
		}

		function youTubePlayerPause() {
			//'use strict';
		
			if (playerActive()) {
				player.pauseVideo();
			}
		}

		/**
 * Play.
	*/
		function youTubePlayerPlay() {
			//'use strict';

			if (playerActive()) {
				player.playVideo();
			}
		}

		function youTubePlayerStateValueToDescription(state, unknow) {
			//'use strict';
		
			var STATES = {'-1': 'unstarted',   // YT.PlayerState.
						  '0': 'ended',        // YT.PlayerState.ENDED
						  '1': 'playing',      // YT.PlayerState.PLAYING
						  '2': 'paused',       // YT.PlayerState.PAUSED
						  '3': 'buffering',    // YT.PlayerState.BUFFERING
						  '5': 'video cued'};  // YT.PlayerState.CUED
		
			return (state in STATES
					? STATES[state]
					: unknow);
		}
		
		function youTubePlayerStop() {
			//'use strict';
		
			if (playerActive()) {
				player.stopVideo();
				player.clearVideo();
			}
		}

		function youTubePlayerVolumeChange(volume) {
			//'use strict';
		
			if (playerActive()) {
				player.setVolume(volume);
			}
		}


		(function () {
			//'use strict';

		
			function init() {
				// Load YouTube library
				var tag = document.createElement('script');
		
				tag.src = 'https://www.youtube.com/iframe_api';
		
				var first_script_tag = document.getElementsByTagName('script')[0];
		
				first_script_tag.parentNode.insertBefore(tag, first_script_tag);
		
		
				// Set timer to display infos
				setInterval(youTubePlayerDisplayInfos, 1000);
			}
		
		
			if (window.addEventListener) {
				window.addEventListener('load', init);
			} else if (window.attachEvent) {
				window.attachEvent('onload', init);
			}
		}());