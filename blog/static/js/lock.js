var os = function () {
  var ua = navigator.userAgent,
    isWindowsPhone = /(?:Windows Phone)/.test(ua),
    isSymbian = /(?:SymbianOS)/.test(ua) || isWindowsPhone,
    isAndroid = /(?:Android)/.test(ua),
    isFireFox = /(?:Firefox)/.test(ua),
    isChrome = /(?:Chrome|CriOS)/.test(ua),
    isTablet = /(?:iPad|PlayBook)/.test(ua) || (isAndroid && !/(?:Mobile)/.test(ua)) || (isFireFox && /(?:Tablet)/.test(ua)),
    isPhone = /(?:iPhone)/.test(ua) && !isTablet,
    isPc = !isPhone && !isAndroid && !isSymbian;
  return {
    isTablet: isTablet,
    isPhone: isPhone,
    isAndroid: isAndroid,
    isPc: isPc
  }
}()

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function getToken() {
  let value = getCookie('UM_distinctid')
  if (!value) {
    return defaultToken
  }
  return value.substring(value.length - 6).toUpperCase()
}

var locked = false
var articleSelector = 'article.article-content'
var defaultToken = 'GERMEY'

$(articleSelector).ready(function () {
  var articleElement = $(articleSelector)[0]

  if (articleElement) {
    var height = articleElement.clientHeight
    var halfHeight = height * 0.3
    var token = getToken()
    $('#locker').find('.token').text(token)

    function detect() {
      console.log('Detecting Token', token)
      $.ajax({
        url: 'https://weixin.cuiqingcai.com/api/locked/',
        method: 'GET',
        data: {
          token: token
        },
        success: function (data) {
          console.log('locked', data.locked)
          if (data.locked === true || data.locked === false) {
            locked = data.locked
          }
        },
        error: function (data) {
          locked = false
        }
      })
    }

    if (os.isPc && halfHeight > 800) {

      detect()
      setInterval(function () {
        detect()
      }, 5000)

      setInterval(function () {
        if (locked && $('#unlock-tag').text() && parseInt($('#unlock-tag').text()) !== 1) {
          $(articleSelector).css('height', halfHeight + 'px')
          $(articleSelector).addClass('lock')
          $('#locker').css('display', 'block')
        } else {
          $(articleSelector).css('height', 'initial')
          $(articleSelector).removeClass('lock')
          $('#locker').css('display', 'none')
        }
      }, 500)

    } else {
      console.log('Lock did not work at', os)
    }

  }
})
