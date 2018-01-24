var EndlessScroll;

EndlessScroll = (function() {
  var defaults;

  EndlessScroll.name = 'EndlessScroll';

  defaults = {
    bottomPixels: 50,
    fireOnce: true,
    fireDelay: 150,
    loader: "Loading...",
    content: "",
    insertAfter: "div:last",
    intervalFrequency: 250,
    resetCounter: function() {
      return false;
    },
    callback: function() {
      return true;
    },
    ceaseFire: function() {
      return false;
    }
  };

  function EndlessScroll(scope, options) {
    var _this = this;
    this.options = $.extend({}, defaults, options);
    this.firing = true;
    this.fired = false;
    this.fireSequence = 0;
    this.didScroll = false;
    this.isScrollable = true;
    this.target = scope;
    this.targetId = "";
    this.content = "";
    this.innerWrap = $(".endless_scroll_inner_wrap", this.target);
    if (this.options.data) {
      this.options.content = this.options.data;
    }
    $(scope).scroll(function() {
      _this.didScroll = true;
      _this.target = scope;
      return _this.targetId = $(_this.target).attr("id");
    });
  }

  EndlessScroll.prototype.run = function() {
    var _this = this;
    return setInterval((function() {
      if (_this.shouldTryFiring()) {
        _this.didScroll = false;
        if (_this.ceaseFireWhenNecessary()) {
          return;
        }
        if (_this.shouldBeFiring()) {
          _this.resetFireSequenceWhenNecessary();
          _this.acknowledgeFiring();
          _this.insertLoader();
          if (_this.hasContent()) {
            _this.showContent();
            _this.fireCallback();
            _this.delayFireingWhenNecessary();
          }
          return _this.removeLoader();
        }
      }
    }), this.options.intervalFrequency);
  };

  EndlessScroll.prototype.shouldTryFiring = function() {
    return this.didScroll && this.firing === true;
  };

  EndlessScroll.prototype.ceaseFireWhenNecessary = function() {
    if (this.options.ceaseFire.apply(this.target, [this.fireSequence])) {
      this.firing = false;
      return true;
    } else {
      return false;
    }
  };

  EndlessScroll.prototype.wrapContainer = function() {
    if (this.innerWrap.length === 0) {
      return this.innerWrap = $(this.target).wrapInner("<div class=\"endless_scroll_inner_wrap\" />").find(".endless_scroll_inner_wrap");
    }
  };

  EndlessScroll.prototype.isScrollableOrNot = function() {
    if (this.target === document || this.target === window) {
      return this.isScrollable = $(document).height() - $(window).height() <= $(window).scrollTop() + this.options.bottomPixels;
    } else {
      this.wrapContainer();
      return this.isScrollable = this.innerWrap.length > 0 && (this.innerWrap.height() - $(this.target).height() <= $(this.target).scrollTop() + this.options.bottomPixels);
    }
  };

  EndlessScroll.prototype.shouldBeFiring = function() {
    this.isScrollableOrNot();
    return this.isScrollable && (this.options.fireOnce === false || (this.options.fireOnce === true && this.fired !== true));
  };

  EndlessScroll.prototype.resetFireSequenceWhenNecessary = function() {
    if (this.options.resetCounter.apply(this.target) === true) {
      return this.fireSequence = 0;
    }
  };

  EndlessScroll.prototype.acknowledgeFiring = function() {
    this.fired = true;
    return this.fireSequence++;
  };

  EndlessScroll.prototype.insertLoader = function() {
    return $(this.options.insertAfter).after("<div class=\"endless_scroll_loader_" + this.targetId + " endless_scroll_loader\">" + this.options.loader + "</div>");
  };

  EndlessScroll.prototype.removeLoader = function() {
    return $(".endless_scroll_loader_" + this.targetId).fadeOut(function() {
      return $(this).remove();
    });
  };

  EndlessScroll.prototype.hasContent = function() {
    if (typeof this.options.content === "function") {
      this.content = this.options.content.apply(this.target, [this.fireSequence]);
    } else {
      this.content = this.options.content;
    }
    return this.content !== false;
  };

  EndlessScroll.prototype.showContent = function() {
    $(this.options.insertAfter).after("<div id=\"endless_scroll_content\">" + this.content + "</div>");
    return $("#endless_scroll_content").hide().fadeIn(250, function() {
      return $(this).removeAttr("id");
    });
  };

  EndlessScroll.prototype.fireCallback = function() {
    return this.options.callback.apply(this.target, [this.fireSequence]);
  };

  EndlessScroll.prototype.delayFireingWhenNecessary = function() {
    var _this = this;
    if (this.options.fireDelay > 0) {
      $("body").after("<div id=\"endless_scroll_marker\"></div>");
      return $("#endless_scroll_marker").fadeTo(this.options.fireDelay, 1, function() {
        $("#endless_scroll_marker").remove();
        return _this.fired = false;
      });
    } else {
      return this.fired = false;
    }
  };

  return EndlessScroll;

})();

(function($) {
  return $.fn.endlessScroll = function(options) {
    return new EndlessScroll(this, options).run();
  };
})(jQuery);


// Script
$(document).ready(function() {
	var offset = $('#numbers li').length;

	$('#numbers').endlessScroll({
		fireOnce: false,
		fireDelay: false,
		loader: '',
		insertAfter: '#numbers li:last',
		content: function(i) {
			return '<li>' + (i + offset) + '</li>';
		}
	});
});
