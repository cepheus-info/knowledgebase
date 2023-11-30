public aspect LoggingAspect {

    pointcut callCustomMethod(int parameter, Clazz acc) : 
     call(boolean Clazz.customMethod(int)) && args(parameter) && target(acc);

    before(int parameter, Clazz acc) : callCustomMethod(parameter, acc) {
    }

    boolean around(int parameter, Clazz acc) : 
      callCustomMethod(parameter, acc) {
        if (acc.value < parameter) {
            return false;
        }
        return proceed(parameter, acc);
    }

    after(int parameter, Clazz acc) : callCustomMethod(parameter, acc) {
    }
}