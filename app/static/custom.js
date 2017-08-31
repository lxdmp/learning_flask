/* 
 * 延时跳转到指定url
 *
 * secs : 延时的秒数;
 * url : 跳转的url;
 * cb_per_sec : 每秒回调;
 * cb_before_jump : 跳转前回调.
 *
 * start : 启动该延时跳转;
 * left : 获取剩余的时间.
 */
function delay_jumper(secs, url, cb_per_sec, cb_before_jump)
{
	_secs = secs+1;
	_url = url;
	_impl = function(){
		if(--_secs>0){
			if(cb_per_sec)
				cb_per_sec();
			setTimeout(_impl, 1000);
		}else{
			if(cb_before_jump)
				cb_before_jump();
			location.href = url;
		}
	};
	_left_secs = function(){
		return _secs;
	}

	return {
		'start' : _impl, 
		'left_secs' : _left_secs
	};
}

