package com.espressif.iot.action.device.common;

import com.espressif.iot.action.IEspActionLocal;
import com.espressif.iot.action.device.IEspActionActivated;
import com.espressif.iot.action.device.IEspActionUnactivated;
import com.espressif.iot.device.IEspDevice;
import com.espressif.iot.type.device.IEspDeviceStatus;

public interface IEspActionDevicePostStatusLocal extends IEspActionActivated, IEspActionUnactivated, IEspActionLocal
{
    /**
     * post the status to device via local
     * 
     * @param device the device
     * @param status the new status
     * @return whether the post action is suc
     */
    boolean doActionDevicePostStatusLocal(final IEspDevice device, final IEspDeviceStatus status);
    
    /**
     * post the status to device( maybe including its child device) via local
     * 
     * @param device the device
     * @param status the new status
     * @param isBroadcast whether post the status to its child or not
     * @return whether the post action is suc
     */
    boolean doActionDevicePostStatusLocal(final IEspDevice device, final IEspDeviceStatus status, boolean isBroadcast);
}
