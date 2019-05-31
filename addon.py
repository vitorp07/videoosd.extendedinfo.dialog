import xbmc
import xbmcgui
import xbmcaddon


def getInfo(infotag):
	return xbmc.getInfoLabel(infotag)

def getCond(condition):
	return xbmc.getCondVisibility(condition)

def getProp(key):
	return xbmcgui.Window(10000).getProperty(key)

def setting(id):
	return xbmcaddon.Addon().getSetting(id)

def execute(function):
	if setting('pause_onclick') == 'true' and getCond('Player.Playing'):
		xbmc.Player().pause()
	xbmc.executebuiltin(function)
	if setting('unpause_onclose') == 'true':
		xbmc.sleep(2000)
		while getProp('infodialogs.active'):
			xbmc.sleep(2000)
		if getCond('Player.Paused'):
			xbmc.Player().pause()

def main():
	if not xbmc.Player().isPlayingVideo():
		return xbmcaddon.Addon().openSettings()
	base = 'RunScript(script.extendedinfo,info='
	info = xbmc.Player().getVideoInfoTag()
	dialog = None
	if getCond('VideoPlayer.Content(movies)'):
		dialog = '{}extendedinfo,imdb_id={},name={})'.format(base, info.getIMDBNumber(), info.getTitle())
	elif getCond('VideoPlayer.Content(episodes)'):
		if setting('episode_infodialog') == 'true' and int(getInfo('System.BuildVersion')[:2]) > 16:
			dialog = '{}extendedepisodeinfo,tvshow={},season={},episode={})'.format(base, info.getTVShowTitle(), info.getSeason(), info.getEpisode())
		else:
			dialog = '{}extendedtvinfo,name={})'.format(base, info.getTVShowTitle())
	if dialog is not None:
		return execute(dialog)


if __name__ == '__main__':
	main()